var attributes = function(neg) {

    if (neg === '') {
        my_common_types = common_types;
        my_common_facts = common_facts;
    }
    else {
        my_common_types = negative_common_types;
        my_common_facts = negative_common_facts;
    }

    for (i = 0; i < $entities_count; i ++ ){
        v_name = "v" + i;
        content = $("<div>").append($("<h3>").text("Common Types:"));
        for (j = 0; j < my_common_types[v_name].length; j ++ ){
            content.append(
                $("<input>")
                .attr("type", "checkbox")
                .attr("name", "type_v" + neg + i)
                .val(j)
            ).append(
                $("<text>").text(cleaner(my_common_types[v_name][j])).append($('<br>')));
        }
        content.append($("<h3>").text("Common Facts:"));
        content.append($("<h4>").text("po_" + v_name));
        for (j = 0; j < my_common_facts[v_name]["facts_po"].length; j++) {
            content.append(
                $("<input>")
                .attr("type", "checkbox")
                .attr("name", "fact_po_v" + neg + i)
                .val(j)
            );
            content.append(
                $("<text>")
                .html("<b>Predicate</b>: " + cleaner(my_common_facts[v_name]["facts_po"][j]["p"])
                    + " <b>Object</b>: " + cleaner(my_common_facts[v_name]["facts_po"][j]["o"]))
            );
            content.append($("<br>"));
        }
        content.append($("<h4>").text("sp_" + v_name));
        for (let j = 0; j < my_common_facts[v_name]["facts_sp"].length; j++) {
            content.append(
                $("<input>")
                .attr("type", "checkbox")
                .attr("name", "fact_sp_v" + neg + i)
                .val(j)
            );
            content.append(
                $("<text>")
                .html("<b>Subject</b>: " + cleaner(my_common_facts[v_name]["facts_sp"][j]["s"])
                    + " <b>Predicate</b>: " + cleaner(my_common_facts[v_name]["facts_sp"][j]["p"]))
            );
            content.append($("<br>"));
        }

        modal_id = '#modal_v' + neg + i;
        if ($(modal_id).length){
            $(modal_id).remove();
        }
        modal_content = $('<div>').addClass('modal fade').
            attr('id', 'modal_v' + neg + i).attr('role', "dialog").
            attr('aria-labelledby', "myModalLabel").attr('aria-hidden', "true")
                .append($('<div>').addClass("modal-dialog")
                    .append($('<div>').addClass("modal-content")
                        .append($('<div>').addClass("modal-header")
                            .append($('<button>').addClass("close").attr("data-dismiss", "modal").attr("aria-hidden", "true").text("X"))
                            .append($('<h4>').addClass("modal-title").text("V" + i)))
                        .append($('<div>').addClass("modal-body").append(content))
                        .append($('<div>').addClass("modal-footer")
                            .append($('<button>').addClass("btn btn-default").attr("data-dismiss", "modal").text("OK")))));
        $('#modal_field').append(modal_content)
    }
};
