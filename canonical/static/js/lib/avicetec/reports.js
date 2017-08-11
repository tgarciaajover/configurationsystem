variables = {
    selected:[],
    obteined:[],
    uniques:[],
    obtain_names:function(variables_source){
        var selected_machines = $.extend(true,[],$.grep(plants_tree.machines, function(e){ return e.selected == true }));
        for(var i in selected_machines){
                delete selected_machines[i].selected;
            }

        $.ajax({
        //type: "POST",
        dataType: "Json",
        url: variables_source,
        //data:selected_machines,
        success:function(data){

                variables.obteined = data.variables.sort();
                data_query.consolidate = $("#bl_consolidate").is(":checked")?"Y":"N";

                if(data_query.consolidate == "Y"){
                    var var_tmp = [];
                    var html_variables = '<div class="col-variables">';
                    for(var i in variables.obteined){
                            var_tmp.push($(variables.obteined[i]).attr("attribute_name"));
                        }
                    variables.uniques = var_tmp.filter(function(item, ind, ar){ return ar.indexOf(item) === ind; }).sort();

                    var available_space = parseInt(variables.uniques.length/6);
                    var counter = 1;
                    for(var i in variables.uniques){
                        html_variables = html_variables + '<div class="checkbox-bird"><input type="checkbox" id="' + variables.uniques[i] + '" name="variables_group"><label for="' + variables.uniques[i] + '">' + variables.uniques[i] + '</label></div>';
                        if(available_space < counter){
                            html_variables = html_variables + '</div><div class="col-variables">';
                            counter = 0;
                            }
                        counter++;
                        }
                    html_variables = html_variables + '</div>';
                    $("#variables_list").empty().html(html_variables);
                    }
                else {
                    var html_variables = '<div class="col-variables-for-machines">';
                    var available_space = parseInt(variables.obteined.length/3);
                    var counter = 1;
                    for(var i in variables.obteined){
                        var id_checkbox = variables.obteined[i].plant+'-'+variables.obteined[i].machine_group+'-'+variables.obteined[i].machine+'-'+variables.obteined[i].attribute_name;
                        html_variables = html_variables + '<div class="checkbox-bird"><input type="checkbox" id="' + id_checkbox + '" name="variables_group"><label for="' + id_checkbox + '">' + variables.obteined[i].plant+'.'+variables.obteined[i].machine+'.'+variables.obteined[i].attribute_name + '</label></div>';
                        if(available_space < counter){
                            html_variables = html_variables + '</div><div class="col-variables-for-machines">';
                            counter = 0;
                            }
                        counter++;
                        }
                    html_variables = html_variables + '</div>';
                    $("#variables_list").empty().html(html_variables);
                    }
                }
            })

        },
    create_query:function(){
        this.selected = [];
        $('input:checkbox[name="variables_group"]:checked').each(function() {
            variables.selected.push($(this).attr('id'));
            });
        var query_machines = [];
        for(var i in this.selected){
                if(data_query.consolidate == "Y"){
                    var qm_tmp = $.extend(true,[],$.grep(this.obteined, function(e){ return e.attribute_name == variables.selected[i] }));
                    }
                else{
                    var var_components = this.selected[i].split("-");
                    var qm_tmp = $.extend(true,[],$.grep(this.obteined, function(e){ return e.plant == var_components[0] && e.machine_group == var_components[1] && e.machine == var_components[2] && e.attribute_name == var_components[3] }));
                    }
                $.merge(query_machines,qm_tmp);
            }
        data_query.attributes = $.extend(true,[],query_machines);
        this.obtain_variables_data("urlServices");
        },
    obtain_variables_data:function(data_source){
        /*$.ajax({
            type: "POST",
            dataType: "json",
            url: data_source,
            //data:data_query,
            success:function(response){
                alert("entra sucess");*/
                //This line is temporal.
                var response = (data_query.consolidate == "Y")?data_example:data_example_mxm;
                var series = [];
                $("#chartsArea").empty();
                if(data_query.consolidate == "Y"){
                    var consolidate_div = $("<canvas/>",{
                            'class'  : 'card-block',
                            'id'     : 'consolidated_chart'
                        });
                    $("#chartsArea").append(consolidate_div);
                    for(var i in variables.selected){

                        var data_tmp = [];
                        var variable_data = $.grep(response.data, function(e){ return e.attribute_name == variables.selected[i] });
                        var min_value = parseFloat(variable_data[0].value);
                        var max_value = min_value;
                        for(var j in variable_data){
                            data_value = parseFloat(variable_data[j].value);
                            min_value=(min_value > data_value)?data_value:min_value;
                            max_value=(max_value < data_value)?data_value:max_value;
                            data_tmp.push({"x":variable_data[j].datetime,"y":data_value});
                            };
                        series.push({"variable":variables.selected[i],"min":min_value,"max":max_value,"data":data_tmp});
                        }
                    create_chart("consolidated_chart",series);
                    }
                else{
                    //alert(JSON.stringify(variables.selected));
                    $.each(plants_tree.plants,function(ind,plant){
                        if(plant.selected){
                            $("#chartsArea").append(
                                $("<div/>",{
                                    //'class'  : 'card-block',
                                    'id'     : 'charts_' + plant.plant_id
                                    }).html("<header class='card-header card-header-xl'>" + plant.descr + "</header>")
                                );
                            $.each(plant.machine_groups,function(ind_mg,machine_group){
                                if(machine_group.selected){
                                    $('#charts_' + plant.plant_id).append(
                                    $("<div/>",{
                                        //'class'  : 'card-block',
                                        'id'     : 'charts_' + machine_group.machine_group_id
                                        }).html("<header class='card-header card-header-lg'>" + machine_group.descr + "</header>")
                                    );
                                    $.each(machine_group.machines,function(ind_m,machine){
                                        if(machine.selected){
                                            $('#charts_' + machine_group.machine_group_id).append(
                                            $("<div/>",{
                                                //'class'  : 'card-block',
                                                'id'     : 'charts_' + machine.machine_id
                                                }).html('<header class="card-header">' + machine.descr + '</header><canvas id = "chart_' + machine.machine_id + '"></canvas>')
                                            );
                                            }
                                        })
                                    }
                                })
                            }
                        });

                    selected_machines = $.grep(plants_tree.machines, function(e){ return e.selected == true })
                    for(var ind in selected_machines){
                        var machine_variables = $.grep(data_query.attributes, function(e){return e.machine == selected_machines[ind].machine});

                        var series = [];
                        for(var i in machine_variables){
                                var data_tmp = [];
                                var variable_data = [];
                                variable_data = $.grep(response.data, function(e){ return e.plant == machine_variables[i].plant && e.machine_group == machine_variables[i].machine_group && e.machine == machine_variables[i].machine && e.attribute_name == machine_variables[i].attribute_name });
                                //alert(JSON.stringify(variable_data));
                                if(variable_data.length > 0){
                                    var min_value = parseFloat(variable_data[0].value);
                                    var max_value = min_value;
                                    for(var j in variable_data){
                                        data_value = parseFloat(variable_data[j].value);
                                        min_value=(min_value > data_value)?data_value:min_value;
                                        max_value=(max_value < data_value)?data_value:max_value;
                                        data_tmp.push({"x":variable_data[j].datetime,"y":data_value});
                                        };
                                    series.push({"variable":machine_variables[i].attribute_name,"min":min_value,"max":max_value,"data":data_tmp});
                                    }
                                }
                        create_chart("chart_" + selected_machines[ind].machine,series);
                        }
                    }

            /*    },
            error: function(a){
                b = a.responseText.replace("/\\/","");
                alert(JSON.stringify(b));
                //this.success(a.responseText);
		}
            });*/
        }
    }

function bl_consolidate_change(){
    variables.obtain_names("/static/data/variables.json");
    }

bl_consolidate_change();

var reports = {
    list:[
        {
            "name":"Evolución de variables",
            "use_variables":true,
        }
    ]
    }

var chartColors = [
'rgb(255, 99, 132)',
'rgb(255, 159, 64)',
'rgb(255, 205, 86)',
'rgb(75, 192, 192)',
'rgb(54, 162, 235)',
'rgb(153, 102, 255)',
'rgb(201, 203, 207)'
];

window.randomScalingFactor = function() {
	return (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 100);
};

function create_chart(container,series){
    var timeFormat = 'YYYY-MM-DD HH:mm';

    var datasets_received = [],yaxes_conf = [];
    for(var i in series){
        scale_factor = (series[i].max-series[i].min)/3;
        datasets_received.push({
            label:series[i].variable,
            yAxisID:"yAxis_" + i,
            backgroundColor: chartColors[i],
            borderColor: chartColors[i],
            fill:false,
            data:series[i].data
            });

        yaxes_conf.push({
            id:"yAxis_" + i,
            type:"logarithmic",
            ticks:{
                min:series[i].min-scale_factor,
                max:series[i].max+scale_factor
                },
            display: false,
            labelString: 'value'
            });
        }

    var color = Chart.helpers.color;
    var config = {
    type: 'line',
    data: {
        datasets: datasets_received
    },
    options: {
        title:{
            text: 'title'
        },
        scales: {
            xAxes: [{
                type: "time",
                time: {
                format: timeFormat,
                //round: 'hour',
                tooltipFormat: 'll HH:mm'
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Linea de Tiempo'
                }
            }],
            yAxes: yaxes_conf
            },
        }
    };
    var ctx = document.getElementById(container).getContext("2d");
    window.myLine = new Chart(ctx, config);

    }