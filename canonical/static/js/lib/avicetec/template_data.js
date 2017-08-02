plants_tree = {
    plants:[],
    machines:[],
    obtein_plants:function(plants_source){

        $.ajax({
            dataType: "Json",
            url: plants_source,
            success:function(data){
                plants_tree.plants = $.extend(true,[],data.plants);
                var plants_list = [];

                for(var i in plants_tree.plants){
                    plant = plants_tree.plants[i];
                    var machine_group_list=[];

                    for(j in plant.machine_groups){
                        machine_group = plant.machine_groups[j];
                        var machine_list = [];

                        for(k in machine_group.machines){
                            machine = machine_group.machines[k];
                            machine_list.push('<li><span class="lbl"><div class="checkbox-bird green"><input id="' + machine.machine_id + '" type="checkbox" value="3" name="' + machine_group.machine_group_id + '" onchange="plants_tree.obtain_selected_machines(this)"><label for="' + machine.machine_id + '">' + machine.descr + '</label></div></span>');
                            plants_tree.machines.push({"plant": plant.plant_id,"machine_group":machine_group.machine_group_id,"machine":machine.machine_id,"selected":false});
                            }
                        html_machine = machine_list.join("");
                        machine_group_list.push('<li class="purple with-sub"><span><span class="lbl"><div class="checkbox-bird purple"><input id="' + machine_group.machine_group_id + '" type="checkbox" value="2" name="' + plant.plant_id + '" onchange="plants_tree.obtain_selected_machines(this)"><label for="' + machine_group.machine_group_id + '">' + machine_group.descr + '</label></div></span></span><ul>' + html_machine + '</ul></li>');
                        }
                    html_machine_group = machine_group_list.join("");
                    plants_list.push('<li class="grey with-sub"><span class="lbl" style="padding-left: 10px;"><div class="checkbox-bird orange"><input id="' + plant.plant_id + '" type="checkbox" value="1" onchange="plants_tree.obtain_selected_machines(this)"><label for="' + plant.plant_id + '">' + plant.descr + '</label></div></span><ul>' + html_machine_group + '</ul></li>');
                    }
                $("#plant_list").html(plants_list.join( "" ));

                /*
                With this function over side-menu-list is controled the open/close tree. Migrated from app.js
                Begin migration
                */
                $('.side-menu-list li.with-sub').each(function(){
                    var parent = $(this),
                    clickLink = parent.find('>span'),
                    subMenu = parent.find('>ul');
                    clickLink.click(function() {
                        if (parent.hasClass('opened')) {
                            parent.removeClass('opened');
                            subMenu.slideUp();
                            subMenu.find('.opened').removeClass('opened');
                        } else {
                            if (clickLink.parents('.with-sub').size() == 1) {
                                $('.side-menu-list .opened').removeClass('opened').find('ul').slideUp();
                                }
                            parent.addClass('opened');
                            subMenu.slideDown();
                            }
                        });
                    });
                /*End migration*/
                }
            });
        },
    select_machines(group,group_id,selected){
        var find_machines = [];

        if(group == 'plant'){
                find_machines = $.grep(this.machines, function(e){ return e.plant == group_id });
            }

        if(group == 'machine_group'){
                find_machines = $.grep(this.machines, function(e){ return e.machine_group == group_id });
            }

        if(group == 'machine'){
                find_machines = $.grep(this.machines, function(e){ return e.machine == group_id });
            }

        for(var i in find_machines){
            for(var j in this.machines){
                    if(this.machines[j].machine == find_machines[i].machine){
                            this.machines[j].selected = selected;
                        }
                }
            }
        },
    obtain_selected_machines:function(cb_selected){
        checkbox_selected = $(cb_selected);
        selected = (checkbox_selected.is(":checked"))?true:false;

        if(checkbox_selected.val()=="1"){
            plant_id = checkbox_selected.attr('id');
            var machine_groups = $('input:checkbox[name="' + plant_id + '"]');
            machine_groups.prop("checked", selected);
            var plant = $.grep(this.plants, function(e){ return e.plant_id == plant_id; });

            for(var i in plant[0].machine_groups){
                var machine_group = plant[0].machine_groups[i];
                var machines = $('input:checkbox[name="' + machine_group.machine_group_id + '"]');
                machines.prop("checked", selected);
                }
            this.select_machines('plant',plant_id,selected);
            }
        if(checkbox_selected.val()=="2"){
            machine_group_id = checkbox_selected.attr('id');
            var machines = $('input:checkbox[name="' + machine_group_id + '"]');
            machines.prop("checked", selected);
            this.select_machines('machine_group',machine_group_id,selected);
            }
        if(checkbox_selected.val()=="3"){
            machine_id = checkbox_selected.attr('id');
            var machines = $('input:checkbox[id="' + machine_id + '"]');
            machines.prop("checked", selected);
            this.select_machines('machine',machine_id,selected);
            }
        $("#prueba").html(JSON.stringify(this.machines));
        }
    }

data_query = {
    consolidate : 'N'
    }

plants_tree.obtein_plants("/static/data/plants.json");

$(function() {
    function cb(start, end) {
        $('#daterange').val(start.format('MMMM D, YYYY HH:mm') + ' - ' + end.format('MMMM D, YYYY HH:mm'));
        data_query.start_dttm = start.format('YYYY-MM-DD hh.mm.ss.SSSS');
        data_query.end_dttm = end.format('YYYY-MM-DD hh.mm.ss.SSSS');
    }
    var drp_parameters = {
        "timePicker": true,
        ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        "linkedCalendars": false,
        "autoUpdateInput": false,
        "alwaysShowCalendars": true,
        "showWeekNumbers": true,
        "showDropdowns": true,
        "showISOWeekNumbers": true
    }

    $('#div_daterange').daterangepicker(drp_parameters,cb);

    cb(moment().subtract(1, 'month'), moment());

    /*$('.datetimepicker-1').datetimepicker({
        widgetPositioning: {
            horizontal: 'right'
        },
        debug: false
    });*/

});