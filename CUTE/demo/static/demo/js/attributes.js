var attributes = function() {

    // Build common types:
    $("div.attributes").append($("<div>").addClass("types"));
    $("div.types").append($("<h3>").text("Common Types:"));

    for (let i = 0; i < v_number; i++) {
        let v_name = "v" + i;
        $("div.types").append($("<div>").addClass("types_v" + i));
        $("div.types_v" + i).append($("<h4>").text(v_name));
        for (let j = 0; j < common_types[v_name].length; j++) {
            $("div.types_v" + i).append(
                $("<input>")
                .attr("type", "checkbox")
                .attr("name", "type_v" + i)
                .val(j)
            );
            $("div.types_v" + i).append(
                $("<text>").text(cleaner(common_types[v_name][j]))
            );
            $("div.types_v" + i).append($("<br>"));
        }
    }

    // Build common facts:
    $("div.attributes").append($("<div>").addClass("facts"));
    $("div.facts").append($("<h3>").text("Common Facts:"));

    for (let i = 0; i < v_number; i++) {
        let v_name = "v" + i;
        $("div.facts").append($("<div>").addClass("facts_v" + i));

        $("div.facts").append($("<div>").addClass("facts_po_v" + i));
        $("div.facts_po_v" + i).append($("<h4>").text("po_" + v_name));
        for (let j = 0; j < common_facts[v_name]["facts_po"].length; j++) {
            $("div.facts_po_v" + i).append(
                $("<input>")
                .attr("type", "checkbox")
                .attr("name", "fact_po_v" + i)
                .val(j)
            );
            $("div.facts_po_v" + i).append(
                $("<text>")
                .html("<b>Predicate</b>: " + cleaner(common_facts[v_name]["facts_po"][j]["p"])
                    + " <b>Object</b>: " + cleaner(common_facts[v_name]["facts_po"][j]["o"]))
            );
            $("div.facts_po_v" + i).append($("<br>"));
        }

        $("div.facts").append($("<div>").addClass("facts_sp_v" + i));
        $("div.facts_sp_v" + i).append($("<h4>").text("sp_" + v_name));
        for (let j = 0; j < common_facts[v_name]["facts_sp"].length; j++) {
            $("div.facts_sp_v" + i).append(
                $("<input>")
                .attr("type", "checkbox")
                .attr("name", "fact_sp_v" + i)
                .val(j)
            );
            $("div.facts_sp_v" + i).append(
                $("<text>")
                .html("<b>Subject</b>: " + cleaner(common_facts[v_name]["facts_sp"][j]["s"])
                    + " <b>Predicate</b>: " + cleaner(common_facts[v_name]["facts_sp"][j]["p"]))
            );
            $("div.facts_sp_v" + i).append($("<br>"));
        }
    }

    // Build a 'Submit' button:
    $("div.attributes").append($("<div>").addClass("submit"));
    $("div.attributes div.submit").append($("<button>").text("submit").attr("id", "attributes_submit"));
    $("div.attributes div.submit").append(
        $("<img src='/static/demo/images/ui-anim_basic_16x16.gif'>")
        .addClass("attributes_submitting")
        .hide()
    );

    $("#attributes_submit").click(function() {
        $("div.results, div.sparql").empty();
    });

    // Ajax for submitting
    $("#attributes_submit").click(function() {
        selected_common_types = {};
        selected_common_facts = {};
        let empty_flag = true;
        for (let i = 0; i < v_number; i++) {
            let v_name = "v" + i;
            selected_common_types[v_name] = new Array();
            $("input[name=type_v" + i + "]:checked").each(function() {
                selected_common_types[v_name].push(common_types[v_name][$(this).val()]);
                empty_flag = false;
            });

            let selected_common_facts_po = new Array();
            $("input[name=fact_po_v" + i + "]:checked").each(function() {
                selected_common_facts_po.push(common_facts[v_name]["facts_po"][$(this).val()]);
                empty_flag = false;
            });

            let selected_common_facts_sp = new Array();
            $("input[name=fact_sp_v" + i + "]:checked").each(function() {
                selected_common_facts_sp.push(common_facts[v_name]["facts_sp"][$(this).val()]);
                empty_flag = false;
            });

            selected_common_facts[v_name] = {
                "facts_po": selected_common_facts_po,
                "facts_sp": selected_common_facts_sp
            };
        }

        // Check if non-selection and empty-pattern
        if (empty_flag && JSON.stringify(common_pattern) == '{}') {
            alert("Sorry, we cannot identify your intents.\nPlease select at least 1 attribute above. :)");
            return;
        }

        let payload = {
            "v_number": v_number,
            "types": selected_common_types,
            "facts": selected_common_facts,
            "pattern": common_pattern,
            "limit": 50,
            "offset": 0
        };

        console.log(JSON.stringify(payload));

        $.ajax({
            type: "POST",
            url: "/demo/query-positive/",
            data: JSON.stringify(payload),
            dataType: "json",
            beforeSend: function() {
                $("button").attr("disabled", true);
                $("img.attributes_submitting").show();
            },
            success: function(data) {
                sparql = data["sparql"];
                results = data["results"];
                console.log(sparql, results);
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
};

