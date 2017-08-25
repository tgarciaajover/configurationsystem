stop_reasons = {
    selected:[],
    obtained:[],
    uniques:[],
    obtain_names:function(reasons_source){
        var selected_machines = $.extend(true,[],$.grep(plants_tree.machines, function(e){ return e.selected == true }));
        $.ajax({
        //type: "POST",
        dataType: "Json",
        url: reasons_source,
        //data:selected_machines,
        success:function(data){

            stop_reasons.obtained = _.sortBy( data.stop_reasons, function(reason) {
                                        return [reason.descr,reason.plant_id].join("_");
                                    });

            var reasons_tmp = [];
            var html_reasons = '<div class="col-variables">';
            for(var i in stop_reasons.obtained){
                var label = $(stop_reasons.obtained[i]).attr("descr") + " (" + $(stop_reasons.obtained[i]).attr("availability_flag") + ")";
                reasons_tmp.push({"id":$(stop_reasons.obtained[i]).attr("id"),"label":label});
                }
            stop_reasons.uniques = reasons_tmp.filter(function(item, ind, ar){ return ar.indexOf(item) === ind; }).sort();
            var available_space = parseInt(stop_reasons.uniques.length/3);
            var counter = 1;
            for(var i in stop_reasons.uniques){
                html_reasons = html_reasons + '<div class="checkbox-bird"><input type="checkbox" id="' +
                               stop_reasons.uniques[i].id + '" name="reasons_group"><label for="' +
                               stop_reasons.uniques[i].id + '">' + stop_reasons.uniques[i].label + '</label></div>';
                if(available_space < counter){
                    html_reasons = html_reasons + '</div><div class="col-variables">';
                    counter = 0;
                    }
                counter++;
                }
            html_reasons = html_reasons + '</div>';
            $("#reasons_list").empty().html(html_reasons);
            }
        });
        },
        create_query:function(report){
            this.selected = [];
            data_query.stop_reasons = [];
            var selected_machines = $.extend(true,[],$.grep(plants_tree.machines, function(e){ return e.selected == true }));
            $('input:checkbox[name="reasons_group"]:checked').each(function() {
                stop_reasons.selected.push($(this).attr('id'));
                });

            for(var i in this.selected){
                for(var j in selected_machines){
                    data_query.stop_reasons.push({"id":this.selected[i],"plant_id":selected_machines[j].plant,"machine_group_id":selected_machines[j].machine_group,"machine_id":selected_machines[j].machine});
                    }
                }
            this.obtain_reasons_data(reports[report].url_data);
            },
        obtain_reasons_data:function(data_source){
        $.ajax({
            type: "POST",
            dataType: "json",
            url: data_source,
            //data:data_query.stop_reasons,
            success:function(response){
                $("#chartsArea").append('<div class="row">' +
                                        '<div id="previous_container" class="col-lg-4">' +
                                        '    <header class="card-header">Perdiodo anterior</header>' +
                                        '    <canvas id="previous_chart" class="canvas-hbc"></canvas>' +
                                        '</div>' +
                                        '<div id="previous_to_date_container" class="col-lg-4">' +
                                        '    <header class="card-header">Anterior a la misma fecha</header>' +
                                        '    <canvas id="previous_to_date_chart" class="canvas-hbc"></canvas>' +
                                        '</div>' +
                                        '<div id="current_container" class="col-lg-4">' +
                                        '    <header class="card-header">Actualmente</header>' +
                                        '    <canvas id="current_chart" class="canvas-hbc"></canvas>' +
                                        '</div>');
                var data_previous_day = [],
                    data_previous_week = [],
                    data_previous_month = [],
                    data_previous_to_date_day = [],
                    data_previous_to_date_week = [],
                    data_previous_to_date_month = [],
                    data_current_day = [],
                    data_current_week = [],
                    data_current_month = [],
                    tooltip_previous_day = [],
                    tooltip_previous_week = [],
                    tooltip_previous_month = [],
                    tooltip_previous_to_date_day = [],
                    tooltip_previous_to_date_week = [],
                    tooltip_previous_to_date_month = [],
                    tooltip_current_day = [],
                    tooltip_current_week = [],
                    tooltip_current_month = [],
                    stop_reasons = [];
                var sr_data = response.data;
                for(var i in sr_data){
                    stop_reasons.push(sr_data[i].id);
                    data_previous_day.push(parseFloat(sr_data[i].previous_day.total));
                    data_previous_week.push(parseFloat(sr_data[i].previous_week.total));
                    data_previous_month.push(parseFloat(sr_data[i].previous_month.total));
                    data_previous_to_date_day.push(parseFloat(sr_data[i].previous_to_date_day.total));
                    data_previous_to_date_week.push(parseFloat(sr_data[i].previous_to_date_week.total));
                    data_previous_to_date_month.push(parseFloat(sr_data[i].previous_to_date_month.total));
                    data_current_day.push(parseFloat(sr_data[i].current_day.total));
                    data_current_week.push(parseFloat(sr_data[i].current_week.total));
                    data_current_month.push(parseFloat(sr_data[i].current_month.total));
                    tooltip_previous_day.push(sr_data[i].previous_day);
                    tooltip_previous_week.push(sr_data[i].previous_week);
                    tooltip_previous_month.push(sr_data[i].previous_month);
                    tooltip_previous_to_date_day.push(sr_data[i].previous_to_date_day);
                    tooltip_previous_to_date_week.push(sr_data[i].previous_to_date_week);
                    tooltip_previous_to_date_month.push(sr_data[i].previous_to_date_month);
                    tooltip_current_day.push(sr_data[i].current_day);
                    tooltip_current_week.push(sr_data[i].current_week);
                    tooltip_current_month.push(sr_data[i].current_month);
                    };
                var data_previous = [
                    { name:"Dia",values:data_previous_day,tooltip:tooltip_previous_day },
                    { name:"Semana",values:data_previous_week,tooltip:tooltip_previous_week },
                    { name:"Mes",values:data_previous_month,tooltip:tooltip_previous_month }
                    ];
                var data_previous_to_date = [
                    { name:"Dia",values:data_previous_to_date_day,tooltip:tooltip_current_day },
                    { name:"Semana",values:data_previous_to_date_week,tooltip:tooltip_previous_to_date_week },
                    { name:"Mes",values:data_previous_to_date_month,tooltip:tooltip_previous_to_date_month }
                    ];
                var data_current = [
                    { name:"Dia",values:data_current_day,tooltip:tooltip_current_day },
                    { name:"Semana",values:data_current_week,tooltip:tooltip_current_week },
                    { name:"Mes",values:data_current_month,tooltip:tooltip_current_month }
                    ]
                create_horizontalBarChart("previous_chart",stop_reasons,data_previous);
                create_horizontalBarChart("previous_to_date_chart",stop_reasons,data_previous_to_date);
                create_horizontalBarChart("current_chart",stop_reasons,data_current);
                }
            });
        }
    }

function create_horizontalBarChart(container,labels,obtained_data){
    var horizontalBarChartData = {
        labels: labels,
        datasets: [{
            label: obtained_data[0].name,
            backgroundColor: chartColors[0],
            borderColor: chartColors[0],
            borderWidth: 1,
            data: obtained_data[0].values
        }, {
            label: obtained_data[1].name,
            backgroundColor: chartColors[1],
            borderColor: chartColors[1],
            data: obtained_data[1].values
        },{
            label: obtained_data[2].name,
            backgroundColor: chartColors[2],
            borderColor: chartColors[2],
            data: obtained_data[2].values
        }]

    };

    var ctx = document.getElementById(container).getContext("2d");
    window.myHorizontalBar = new Chart(ctx, {
        type: 'horizontalBar',
        data: horizontalBarChartData,
        options: {
            tooltips: {
                    //mode: 'index',
                    callbacks: {
                        // Use the footer callback to display the sum of the items showing in the tooltip
                        footer: function(tooltipItems, data) {
                            var aditional_fields = "Actual: " + obtained_data[tooltipItems[0].datasetIndex].tooltip[tooltipItems[0].datasetIndex].currencies +
                                                   " Promedio: " + obtained_data[tooltipItems[0].datasetIndex].tooltip[tooltipItems[0].datasetIndex].avg +
                                                   " Variación: " + obtained_data[tooltipItems[0].datasetIndex].tooltip[tooltipItems[0].datasetIndex].var
                            return aditional_fields;
                        },
                    },
                    footerFontStyle: 'normal'
                },
            elements: {
                rectangle: {
                    borderWidth: 2,
                }
            },
            responsive: true,
            scales: {
                xAxes: [{
                    ticks:{ min:0 }
                    }]
                }
        }
    });
    }