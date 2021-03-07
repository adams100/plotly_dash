



// Grab a reference to the dropdown select element
var vendors = d3.select("#drop1");
var dropbutton = vendors.append("button")
    .attr("class", "btn btn-secondary dropdown-toggle")
    .attr("type", "button") 
    .attr("id", "dropdownMenuButton1")
    .attr("data-toggle", "dropdown")
    .attr("aria-haspopup", "true")
    .attr("aria-expandex", "false")
    .text("Vendor");

    vendors.append("div")
    .attr("id", "drop1_1")
    .attr("class", "dropdown-menu")
    .attr("aria-labelledby", "dropdownMenuButton");


var drop1_1 = d3.select("#drop1_1");

d3.json("/vendornames").then(function(n) {
    n.forEach(function (x) {
        drop1_1.append("a")
        .text(x)
        .property("value", x)
        .attr("class", "dropdown-item")
        .on("click", function() { 
            d3.select("#dropdownMenuButton1")
            .text(d3.select(this)
                    .text());
            });
    });
});


// Grab a reference to the dropdown select element
var vendors = d3.select("#drop2");
var dropbutton = vendors.append("button")
    .attr("class", "btn btn-secondary dropdown-toggle")
    .attr("type", "button") 
    .attr("id", "dropdownMenuButton2")
    .attr("data-toggle", "dropdown")
    .attr("aria-haspopup", "true")
    .attr("aria-expandex", "false")
    .text("Year");

    vendors.append("div")
    .attr("id", "drop2_1")
    .attr("class", "dropdown-menu")
    .attr("aria-labelledby", "dropdownMenuButton");

// Use the list of sample names to populate the select options



var drop2_1 = d3.select("#drop2_1");

d3.json("/dates").then(function(n) {
    n.forEach(function (x) {
        drop2_1.append("a")
        .text(x)
        .property("value", x)
        .attr("class", "dropdown-item")
        .on("click", function() { 
            d3.select("#dropdownMenuButton2")
            .text(d3.select(this)
                    .text());
            });
    });
});




function generateChart() {
    document.getElementById("plotarea").innerHTML = "";

    var vendor = d3.select("#dropdownMenuButton1").text();

    var date = d3.select("#dropdownMenuButton2").text();
    console.log(vendor, date);
    var colheaders = ["Document Id", "Document Number", "Vendor", "Vendor Name", "Total Amt in Doc Curr", "Posting date", "Purchasing Document"];

    var request = d3.json("/filtered_data", {
        method: "POST",
        headers: {"Content-Type": "application/json" },
        body: JSON.stringify({
            "vendor": vendor,
            "date": date})
        }); 

    
    request.then(function(x) {
        var tarea = d3.select("#invoicelistview");
        tarea.selectAll("*").remove();
        
        var table = tarea.append("table")
            .style("border-collapse", "collapse")
            .style("border", "1px black solid")
            .attr("class", "table");
    
        var thead = table.append("thead").attr("class", "thead-dark");
        
        
        thead.selectAll("tr")     
            .data(colheaders)
            .enter()
            .append("th")
            .style("border-collapse", "collapse")
            .style("border", "1px black solid") 
            .text(function(x) {return x;});
        

        var tbody = table.append("tbody");

        for (var u = 0; u < x.Document_Id.length; u++) {
            var row =tbody.append("tr");
            row.selectAll("td")
                .data([x.Document_Id[u], x.Document_Number[u], x.Vendor_Number[u], x.Vendor_Name[u], x.Total_Amount[u], x.Posting_date[u], x.Purchasing_Document[u]])
                .enter()
                .append("td")
                .style("border-collapse", "collapse")
                .style("border", "1px black solid") 
                .style("text-align", "center")
                .style("padding", "5px")
                .text(function(e) {return e;});
        }
        
        d3.select("#header")
            .text("Invoice List");
        var plot_request = d3.json("/plotdata", {
            method: "POST",
            headers: {"Content-Type": "application/json" },
            body: JSON.stringify({
                "plotme": "iight bro",
                "vendor": vendor,
                "date": date})
            }); 



        // transform tickvals to scale 

        plot_request.then(function(d) {
            
            //transform x to scale
            var x_transformed = [];
            for(var t = 0; t < d.x.length; t++) 
            {
                for (var r = 0; r < d.xtick_vals.length; r++)
                {
                    if (d.x[t] == d.xtick_vals[r])
                    {
                        x_transformed.push(r);
                        break;
                    }
                }
            }

            //transform tickvals to 1, 2, 3, 4...
            tickvals_transformed = [];
            for (var q = 0; q < d.xtick_vals.length; q++)
            {
                tickvals_transformed.push(q);
            }

            //get largest value for size
           var largest = 0;
            d.y.forEach(function (v) {
                if (largest < v) {
                    largest = v;
                }
            });
            //calc size
            sizes = [];
            d.y.forEach(function(values) {
                sizes.push(100*(values/largest));
            });

            // hovertext
            txt = [];
            for (var n = 0; n < d.x.length; n++) 
            {
                var price = d.y[n].toFixed(2);
                txt.push("Document#: " + d.doc_num[n] + "<br>Date: " + d.x[n] + "<br>Value: $" + price);
            }
            var data = [{
                x: x_transformed,
                y: d.y,
                mode: 'markers',
                marker: {
                    size: sizes,
                    opacity: d.o
                },
                text: txt,
                hoverinfo: "text",
                // hovertemplate: "%{d.x}",
                type: 'scatter'
            }];
            var layout = {
                height: 650,
                width: 1500,
                title: "Vendor Spend",
                xaxis: {
                    tickvals: tickvals_transformed,
                    ticktext: d.xtick_labels,
                    rangemode: "tozero"
                }
            };
            Plotly.newPlot("plotarea", data, layout);   
        });
    });
}
