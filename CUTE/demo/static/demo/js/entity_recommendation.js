var entity_recommendation = function() {

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
                    console.log(data);
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
            console.log(ui.item);
        }
    }

    $("input[type='text']").autocomplete(entity_recommendation_dict);

    $("#add_col, #del_col, #add_row, #del_row, #entity_submit").click(function() {
        $("div.attributes, div.results, div.pattern, div.sparql").empty();
    });

    $("#add_col").click(function() {
        if (v_number == MAX_COLUMN) {
            alert("Too many columns!");
            return;
        }
        $("button").attr("disabled", true);
        $("table.input_table tr.title").append($("<th>").text("v" + v_number));
        for (let i = 0; i < row_number; i++)
            $("table.input_table tr.row_" + i).append(
                $("<td>")
                .append(
                    $("<input>")
                    .attr("type", "text")
                    .attr("name", "entity_" + i + "_" + v_number)
                    .addClass("unselected")
                    .autocomplete(entity_recommendation_dict)
                )
            );
        v_number++;
        $("button").attr("disabled", false);
    });

    $("#del_col").click(function() {
        if (v_number == 1) {
            alert("Only one column exists!");
            return;
        }
        $("button").attr("disabled", true);
        $("th:last-child").remove();
        $("td:last-child").remove();
        v_number--;
        $("button").attr("disabled", false);
    });

    $("#add_row").click(function() {
        if (row_number == MAX_ROW) {
            alert("Too many rows!");
            return;
        }
        $("button").attr("disabled", true);
        $("table.input_table").append($("<tr>").addClass("row_" + row_number));
        for (let i = 0; i < v_number; i++)
            $("table.input_table tr.row_" + row_number).append(
                $("<td>")
                .append(
                    $("<input>")
                    .attr("type", "text")
                    .attr("name", "entity_" + row_number + "_" + i)
                    .addClass("unselected")
                    .autocomplete(entity_recommendation_dict)
                )
            );
        row_number++;
        $("button").attr("disabled", false);
    });

    $("#del_row").click(function() {
        if (row_number == 1) {
            alert("Only one row exists!");
            return;
        }
        $("button").attr("disabled", true);
        $("tr:last-child").remove();
        row_number--;
        $("button").attr("disabled", false);
    });

    $("#entity_submit").click(function() {

        let entities = [];
        let if_all_selected = true;
        for (let i = 0; i < row_number; i++) {
            let row_entities = [];
            for (let j = 0; j < v_number; j++) {
                let input_ele_name = "input[name='entity_" + i + "_" + j + "']";
                if ($(input_ele_name).hasClass("selected") == false) {
                    $(input_ele_name).removeClass("unselected").addClass("unselected_error");
                    if_all_selected = false;
                }

                row_entities.push($(input_ele_name).val());
            }
            entities.push(row_entities);
        }
        if (if_all_selected == false)
            return;

        let payload = {
            "row_number": row_number,
            "v_number": v_number,
            "entities": entities
        }

        console.log(JSON.stringify(payload));



        let find_attributes = $.ajax({
            type: "POST",
            url: "/demo/attributes/",
            data: JSON.stringify(payload),
            dataType: "json",
            beforeSend: function() {
                $("button").attr("disabled", true);
                $("img.entity_submitting").show();
            }
        });

        let find_pattern = $.ajax({
            type: "POST",
            url: "/demo/pattern/",
            data: JSON.stringify(payload),
            dataType: "json",
            beforeSend: function() {
                $("button").attr("disabled", true);
                $("img.entity_submitting").show();
            }
        });

        $.when(find_attributes, find_pattern).then(function(attributes_data, pattern_data) {
            common_types = attributes_data[0]["types"];
            common_facts = attributes_data[0]["facts"];
            common_pattern = pattern_data[0]["pattern"];
            console.log(common_types, common_facts, common_pattern);
            attributes();
            pattern();
            $("button").attr("disabled", false);
            $("img.entity_submitting").hide();
        }, function(err1, err2) {
            console.log(err1);
            console.log(err2);
            $("button").attr("disabled", false);
            $("img.entity_submitting").hide();
        });
    });
};
