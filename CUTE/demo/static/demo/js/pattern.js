var pattern = function() {
    $("div.pattern").append($("<h3>").text("Pattern"));

    for (let i = 0; i < v_number; i++)
        for (let j = i + 1; j < v_number; j++) {
            let r_name = "r_" + i + "_" + j;
            $("div.pattern").append($("<div>").addClass(r_name));
            $("div." + r_name).append($("<h4>").text("Path v" + i + " to v" + j));

            for (let k = 0; k < common_pattern[r_name].length; k++) {
                $("div." + r_name).append($("<p>").text(JSON.stringify(common_pattern[r_name][k])));
            }
        }
};
