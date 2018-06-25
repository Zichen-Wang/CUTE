var attributes = function(neg) {
    let my_common_types, my_common_facts;
    let selected_common_types = {};
    let selected_common_facts = {};

    if (neg === '') {
        my_common_types = common_types;
        my_common_facts = common_facts;

        for (let i = 0; i < $entities_count; i++) {
            let v_name = "v" + i;

            selected_common_types[v_name] = new Set();
            if (old_common_types !== undefined) {
                $("input[name=type_v" + i + "]:checked").each(function() {
                    selected_common_types[v_name].add(old_common_types[v_name][$(this).val()]);
                });
            }
            let selected_common_facts_po = new Set();
            let selected_common_facts_sp = new Set();

            if (old_common_facts !== undefined) {
                $("input[name=fact_po_v" + i + "]:checked").each(function() {
                    selected_common_facts_po.add(old_common_facts[v_name]["facts_po"][$(this).val()]);
                });

                $("input[name=fact_sp_v" + i + "]:checked").each(function() {
                    selected_common_facts_sp.add(old_common_facts[v_name]["facts_sp"][$(this).val()]);
                });
            }


            selected_common_facts[v_name] = {
                "facts_po": selected_common_facts_po,
                "facts_sp": selected_common_facts_sp
            };
        }
    }

    else {
        my_common_types = negative_common_types;
        my_common_facts = negative_common_facts;

        for (let i = 0; i < $entities_count; i++) {
            let v_name = "v" + i;

            selected_common_types[v_name] = new Set();
            if (old_negative_common_types !== undefined) {
                $("input[name=type_v_neg" + i + "]:checked").each(function() {
                    selected_common_types[v_name].add(old_negative_common_types[v_name][$(this).val()]);
                });
            }

            let selected_common_facts_po = new Set();
            let selected_common_facts_sp = new Set();

            if (old_negative_common_facts !== undefined) {

                $("input[name=fact_po_v_neg" + i + "]:checked").each(function() {
                    selected_common_facts_po.add(
                        old_negative_common_facts[v_name]["facts_po"][$(this).val()]["p"]
                        + 
                        "_*_"
                        +
                        old_negative_common_facts[v_name]["facts_po"][$(this).val()]["o"]
                    );
                });

                $("input[name=fact_sp_v_neg" + i + "]:checked").each(function() {
                    selected_common_facts_sp.add(
                        old_negative_common_facts[v_name]["facts_sp"][$(this).val()]["s"]
                        +
                        "_*_"
                        +
                        old_negative_common_facts[v_name]["facts_sp"][$(this).val()]["o"]
                    );
                });
            }

            selected_common_facts[v_name] = {
                "facts_po": selected_common_facts_po,
                "facts_sp": selected_common_facts_sp
            };
        }

    }

    for (let i = 0; i < $entities_count; i ++ ){
        let v_name = "v" + i;
        let content = $("<div>").append($("<h4>").text("Common Types:"));
        let modal_id = '#modal_v' + neg + i;


        if ($(modal_id).length) {
            
            $(modal_id).remove();
        }
        if (neg !== '' && count_all_row_neg() === 0)
            continue;

        for (let j = 0; j < my_common_types[v_name].length; j ++ ){
            let $type = $("<input>")
                .attr("type", "checkbox")
                .attr("name", "type_v" + neg + i)
                .val(j);

            if (selected_common_types[v_name].has(my_common_types[v_name][j]))
                $type.prop("checked", "true");

            if (neg === '' && j === my_common_types[v_name].length - 1)
                $type.prop("checked", "true");

            if (neg !== '' && j === 0)
                $type.prop("checked", "true");

            content.append($type);
            content.append(
                $("<text>").text(" " + cleaner(my_common_types[v_name][j])).append($('<br>')));
        }
        content.append($("<hr>"));
        content.append($("<h4>").text("Common Facts:"));
        // content.append($("<h5>").text("po_" + v_name));
        for (let j = 0; j < my_common_facts[v_name]["facts_po"].length; j++) {
            let $fact = $("<input>")
                .attr("type", "checkbox")
                .attr("name", "fact_po_v" + neg + i)
                .val(j);

            if (selected_common_facts[v_name]["facts_po"].has(
                    my_common_facts[v_name]["facts_po"][j]["p"]
                    +
                    "_*_"
                    +
                    my_common_facts[v_name]["facts_po"][j]["o"]
                )
            )
                $fact.prop("checked", "true");

            content.append($fact);
            content.append(
                $("<text>")
                .html("<b> Predicate</b>: " + cleaner(my_common_facts[v_name]["facts_po"][j]["p"])
                    + " <b> Object</b>: " + cleaner(my_common_facts[v_name]["facts_po"][j]["o"]))
            );
            content.append($("<br>"));
        }
        content.append($("<br>"));
        // content.append($("<h5>").text("sp_" + v_name));
        for (let j = 0; j < my_common_facts[v_name]["facts_sp"].length; j++) {
            let $fact = $("<input>")
                .attr("type", "checkbox")
                .attr("name", "fact_sp_v" + neg + i)
                .val(j);

            if (selected_common_facts[v_name]["facts_sp"].has(
                    my_common_facts[v_name]["facts_sp"][j]["s"]
                    +
                    "_*_"
                    +
                    my_common_facts[v_name]["facts_sp"][j]["p"]
                )
            )
                $fact.prop("checked", "true");

            content.append($fact);
            content.append(
                $("<text>")
                .html("<b> Subject</b>: " + cleaner(my_common_facts[v_name]["facts_sp"][j]["s"])
                    + " <b> Predicate</b>: " + cleaner(my_common_facts[v_name]["facts_sp"][j]["p"]))
            );
            content.append($("<br>"));
        }

        let modal_content = $('<div>').addClass('modal fade').
            attr('id', 'modal_v' + neg + i).attr('role', "dialog").
            attr('aria-labelledby', "myModalLabel").attr('aria-hidden', "true")
                .append($('<div>').addClass("modal-dialog")
                    .append($('<div>').addClass("modal-content")
                        .append($('<div>').addClass("modal-header")
                            .append($('<button>').addClass("close").attr("data-dismiss", "modal").attr("aria-hidden", "true").text("x"))
                            .append($('<h3>').addClass("modal-title").text("Attributes for v" + i)))
                        .append($('<div>').addClass("modal-body").append(content))
                        .append($('<div>').addClass("modal-footer")
                            .append($('<button>').addClass("btn btn-default").attr("data-dismiss", "modal").text("OK")))));
        $('#modal_field').append(modal_content)
    }
};
