$(document).ready(function () {

    let entity_recommendation_dict = {
        source: function(request, response) {
            $.ajax({
                type: "POST",
                url: "/demo/entity-recommendation/",
                data: JSON.stringify({
                    "input_name": request.term,
                    "top_k": 10
                }),
                dataType: "json",
                success: function(data) {
                    response(data["mapped_entities"]);
                }
            });
        },
        autoFocus: true,
        response: function(event, ui) {
            $(this).removeClass("selected").removeClass("unselected_error").addClass("unselected");
        },
        close: function(event, ui) {
            if ($(this).hasClass("unselected"))
                $(this).removeClass("unselected").addClass("unselected_error");
        },
        select: function(event, ui) {
            $(this).removeClass("unselected").removeClass("unselected_error").addClass("selected");
        }
    };

    $("input[type='text']").autocomplete(entity_recommendation_dict);

    $entities = $('#entities');
    $e_add = $('#entities_add');
    $e_delete = $('#entities_delete');

    $entities_count = 1;
    $all_rows = [];
    $all_rows_neg = [];

    $e_add.click(function (e) {
        if ($entities_count < max_entities_count){
            $entities.append(
                    $("<input>")
                    .attr("type", "text").attr("placeholder", "v" + $entities_count)
                    .addClass("unselected")
                    .autocomplete(entity_recommendation_dict)
                );
            $entities_count += 1;
        }
        return false;
    });

    $e_delete.click(function (e) {
        if ($entities_count > 1) {
            $("#entities input:last-child").remove();
            $entities_count -= 1;
        }
        return false;
    });

    $('#entities_submit').click(function () {
        all_correct = true;
        $all_inputs = $('input[type=text]');
        $all_inputs.each(function () {
            if (!$(this).hasClass('selected'))
            {
                all_correct = false;
                $(this).removeClass('unselected').removeClass('unselected_error').addClass('unselected_error');
            }
        });

        if (!all_correct) return false;

        $entities_add = $('#entities_add');
        if ($entities_add.length !== 0) {
            $entities_add.remove();
            $('#entities_delete').remove();
            $input_entities = $('#input_entities');
            for ($i = 0; $i < $entities_count; $i ++ ){
                $input_entities.append($('<span>').text('V' + $i).attr('name', $i).click(function () {
                    name_v = '#modal_v' + $(this).attr('name');
                    $(name_v).modal({});
                }));
            }
            $input_entities = $('#negvative_entities');
            for ($i = 0; $i < $entities_count; $i ++ ){
                $input_entities.append($('<span>').text('V' + $i).attr('name', $i).click(function () {
                    name_v = '#modal_v_neg' + $(this).attr('name');
                    $(name_v).modal({});
                }));
            }
            $input_entities = $('#results_entities');
            for (i = 0; i < $entities_count; i ++ ){
                $input_entities.append($('<span>').text('V' + i));
            }
        }

        text = "";
        entities_line = [];
        $all_inputs.each(function () {
            text += "<span>" + this.value + "</span>";
            entities_line.push(this.value);
            this.value = '';
            $(this).removeClass('selected').addClass('unselected');
        });
        $all_rows.push(entities_line);

        $('<tr>').append($('<td>').append($('<a>').text('Delete').attr('name', $all_rows.length-1).click(function () {
            $all_rows[parseInt(this.name)] = [];
            this.closest('tr').remove();
            submit_to_server();
            return false;
        }))).append($('<td>').html(text)).insertAfter($('#input_field'));

        submit_to_server();
        return false;
    });

    $all_submit = $('#all_submit');
    $all_submit.click(function() {
        $("div.sparql").empty();
        for (i = 0; i < all_results.length; i ++ ){
            if (all_results[i].length){
                all_results[i].remove();
            }
        }
    });

    // Ajax for submitting
    $all_submit.click(function() {
        selected_common_types = {};
        selected_common_facts = {};
        let empty_flag = false;
        for (let i = 0; i < $entities_count; i++) {
            let v_name = "v" + i;
            flag = true;
            selected_common_types[v_name] = [];
            $("input[name=type_v" + i + "]:checked").each(function() {
                selected_common_types[v_name].push(common_types[v_name][$(this).val()]);
                flag = false;
            });

            let selected_common_facts_po = [];
            $("input[name=fact_po_v" + i + "]:checked").each(function() {
                selected_common_facts_po.push(common_facts[v_name]["facts_po"][$(this).val()]);
                flag = false;
            });

            let selected_common_facts_sp = [];
            $("input[name=fact_sp_v" + i + "]:checked").each(function() {
                selected_common_facts_sp.push(common_facts[v_name]["facts_sp"][$(this).val()]);
                flag = false;
            });

            selected_common_facts[v_name] = {
                "facts_po": selected_common_facts_po,
                "facts_sp": selected_common_facts_sp
            };
            if (flag){
                empty_flag = true;
            }
        }

        selected_common_types_neg = {};
        selected_common_facts_neg = {};
        empty_flag_neg = true;
        has_flag_neg = false;
        for (i = 0; i < $all_rows_neg.length; i ++ ){
            if ($all_rows_neg[i].length > 0){
                has_flag_neg = true;
            }
        }
        for (let i = 0; i < $entities_count; i++) {
            let v_name = "v" + i;
            selected_common_types_neg[v_name] = [];
            $("input[name=type_v_neg" + i + "]:checked").each(function() {
                selected_common_types_neg[v_name].push(negative_common_types[v_name][$(this).val()]);
                empty_flag_neg = false;
            });

            let selected_common_facts_po_neg = [];
            $("input[name=fact_po_v_neg" + i + "]:checked").each(function() {
                selected_common_facts_po_neg.push(negative_common_facts[v_name]["facts_po"][$(this).val()]);
                empty_flag_neg = false;
            });

            let selected_common_facts_sp_neg = [];
            $("input[name=fact_sp_v_neg" + i + "]:checked").each(function() {
                selected_common_facts_sp_neg.push(negative_common_facts[v_name]["facts_sp"][$(this).val()]);
                empty_flag_neg = false;
            });

            selected_common_facts_neg[v_name] = {
                "facts_po": selected_common_facts_po_neg,
                "facts_sp": selected_common_facts_sp_neg
            };
        }

        // Check if non-selection and empty-pattern
        if (empty_flag || (has_flag_neg && empty_flag_neg)) {
            alert("Sorry), we cannot identify your intents.\nPlease select at least 1 attribute above. :)");
            return;
        }

        let payload = {
            "v_number": $entities_count,
            "pos_types": selected_common_types,
            "pos_facts": selected_common_facts,
            "neg_types": selected_common_types_neg,
            "neg_facts": selected_common_facts_neg,
            "pattern": common_pattern,
            "limit": 50,
            "offset": 0
        };

        //console.log("payload --- " + JSON.stringify(payload));

        $.ajax({
            type: "POST",
            url: "/demo/query/",
            data: JSON.stringify(payload),
            dataType: "json",
            beforeSend: function() {
                $("button").attr("disabled", true);
                $("img.attributes_submitting").show();
            },
            success: function(data) {
                sparql = data["sparql"];
                results = data["results"];
                query();
            },
            error: function(err) {
                console.log(err);
            },
            complete: function() {
                $("button").attr("disabled", false);
                $("img.attributes_submitting").hide();
            }
        });
    });
});