var query = function() {

    $("div.sparql").append($("<h3>").text("SPARQL Query"));
    $("div.sparql").append($("<pre>").text(sparql));

    $("div.results").append($("<h3>").text("Results"));

    // Build the results table
    $("div.results").append($("<table>").addClass("results_table"));

    // Build the title row
    $("table.results_table").append($("<tr>").addClass("title"));
    $("table.results_table tr.title").append($("<th>").text("Rej"));
    for (let i = 0; i < v_number; i++)
        $("table.results_table tr.title").append($("<th>").text("v" + i));

    // Build the results row
    for (let i = 0; i < results.length; i++) {
        $("table.results_table").append($("<tr>").addClass("row_" + i));
        $("table.results_table tr.row_" + i).append(
            $("<td>")
            .append(
                $("<input>")
                .attr("type", "checkbox")
                .attr("name", "result")
                .val(i)
            )
        );
        for (let j = 0; j < v_number; j++)
            $("table.results_table tr.row_" + i).append($("<td>").text(results[i]["v" + j]));
    }

    // Build a 'Reject' button
    $("div.results").append($("<div>").addClass("submit"));
    $("div.results div.submit").append($("<button>").text("Reject").attr("id", "reject_submit"));
    $("div.results div.submit").append(
        $("<img src='/static/demo/images/ui-anim_basic_16x16.gif'>")
        .addClass("reject_submitting")
        .hide()
    );

    // Ajax for rejecting
    $("#reject_submit").click(function() {
        negative_results = new Array();

        let empty_flag = true;
        $("input[name=result]:checked").each(function() {
            let one_result_list = new Array();
            let one_result = results[$(this).val()];
            for (let i = 0; i < v_number; i++)
                one_result_list.push(one_result["v" + i]);

            negative_results.push(one_result_list);
            empty_flag = false;
        });

        if (empty_flag) {
            alert("Sorry, please select at least 1 result to reject. :)");
            return;
        }

        let payload = {
            "row_number": negative_results.length,
            "v_number": v_number,
            "entities": negative_results
        }

        console.log(JSON.stringify(payload));

        $.ajax({
            type: "POST",
            url: "/demo/attributes/",
            data: JSON.stringify(payload),
            dataType: "json",
            beforeSend: function() {
                $("button").attr("disabled", true);
                $("img.reject_submitting").show();
            },
            success: function(data) {
                negative_common_types = data["types"];
                negative_common_facts = data["facts"];
                console.log(negative_common_types, negative_common_facts);
                negative_attributes();
            },
            error: function(err) {
                console.log(err);
            },
            complete: function() {
                $("button").attr("disabled", false);
                $("img.reject_submitting").hide();
            }
        });
        
    });
};