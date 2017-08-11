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
                plant = $.grep(this.plants, function(e){ return e.plant_id == group_id });
                plant[0].selected = selected;
                $.each(plant[0].machine_groups, function(i){
                    plant[0].machine_groups[i].selected = selected;
                    $.each(plant[0].machine_groups[i].machines,function(j){
                        plant[0].machine_groups[i].machines[j].selected = selected;
                        })
                    });

            }

        if(group == 'machine_group'){
                find_machines = $.grep(this.machines, function(e){ return e.machine_group == group_id });
                plant = $.grep(this.plants, function(e){ return e.plant_id == find_machines[0].plant });
                plant[0].selected = (selected)?true:$('input:checkbox[id="' +find_machines[0].plant+ '"]').prop("checked");
                machine_group = $.grep(plant[0].machine_groups, function(e){ return e.machine_group_id == group_id });
                machine_group[0].selected = selected;
                $.each(machine_group[0].machines,function(i){
                    machine_group[0].machines[i].selected = selected;
                    })
                }

        if(group == 'machine'){
                find_machines = $.grep(this.machines, function(e){ return e.machine == group_id });
                plant = $.grep(this.plants, function(e){ return e.plant_id == find_machines[0].plant });
                plant[0].selected = (selected)?true:$('input:checkbox[id="' +find_machines[0].plant+ '"]').prop("checked");
                machine_group = $.grep(plant[0].machine_groups, function(e){ return e.machine_group_id == find_machines[0].machine_group });
                machine_group[0].selected = (selected)?true:$('input:checkbox[id="' +find_machines[0].machine_group+ '"]').prop("checked");
                machine = $.grep(machine_group[0].machines, function(e){ return e.machine_id == group_id });
                machine[0].selected = selected;
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
            var plant = $.grep(this.plants, function(e){return e.plant_id == plant_id; });
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
        }
    }

data_query = {
    consolidate : 'N',
    company_id:0,//This value is obteined in the user variables.
    attributes:[]
    }

plants_tree.obtein_plants("/static/data/plants.json");

$(function() {
    function cb(start, end) {
        $('#daterange').val(start.format('MMMM D, YYYY HH:mm') + ' - ' + end.format('MMMM D, YYYY HH:mm'));
        data_query.start_dttm = start.format('YYYY-MM-DD hh.mm.ss.SSSS');
        data_query.end_dttm = end.format('YYYY-MM-DD hh.mm.ss.SSSS');
        diff_days = end.diff(start,"days");

        $("input:radio[name='time_unit']:checked").parent().removeClass("active");
        switch(true){
            case (diff_days == 0):
                $("input:radio[id='rb_na']").prop("checked",true);
                break;
            case (diff_days > 0 && diff_days <= 7)://min:24 points - max: 168 points
                $("input:radio[id='rb_hours']").prop("checked",true);
                break;
            case (diff_days > 7 && diff_days <= 180)://min:8 points - max: 180 points
                $("input:radio[id='rb_days']").prop("checked",true);
                break;
            case (diff_days > 180 && diff_days <= 720)://min:24 points - max: 104 points
                $("input:radio[id='rb_weeks']").prop("checked",true);
                break;
            case (diff_days > 720 && diff_days <= 3600)://min:24 points - max: 120 points
                $("input:radio[id='rb_months']").prop("checked",true);
                break;
            case (diff_days > 3600)://min:5 points
                $("input:radio[id='rb_years']").prop("checked",true);
                break;
            }
        data_query.time_unit = $("input:radio[name='time_unit']:checked").prop("value");
        $("input:radio[name='time_unit']:checked").parent().addClass("active");
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


});