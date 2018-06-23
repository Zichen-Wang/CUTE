var attributes = function(neg) {
    let my_common_types, my_common_facts;
    if (neg === '') {
        my_common_types = common_types;
        my_common_facts = common_facts;
    }
    else {
        my_common_types = negative_common_types;
        my_common_facts = negative_common_facts;
    }

    for (let i = 0; i < $entities_count; i ++ ){
        let v_name = "v" + i;
        let content = $("<div>").append($("<h4>").text("Common Types:"));
        for (let j = 0; j < my_common_types[v_name].length; j ++ ){
            let $type = $("<input>")
                .attr("type", "checkbox")
                .attr("name", "type_v" + neg + i)
                .val(j);
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
            content.append(
                $("<input>")
                .attr("type", "checkbox")
                .attr("name", "fact_po_v" + neg + i)
                .val(j)
            );
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
            content.append(
                $("<input>")
                .attr("type", "checkbox")
                .attr("name", "fact_sp_v" + neg + i)
                .val(j)
            );
            content.append(
                $("<text>")
                .html("<b> Subject</b>: " + cleaner(my_common_facts[v_name]["facts_sp"][j]["s"])
                    + " <b> Predicate</b>: " + cleaner(my_common_facts[v_name]["facts_sp"][j]["p"]))
            );
            content.append($("<br>"));
        }

        let modal_id = '#modal_v' + neg + i;
        if ($(modal_id).length){
            $(modal_id).remove();
        }
        if (neg !== '' && $all_rows_neg.length === 0)
            return;
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
