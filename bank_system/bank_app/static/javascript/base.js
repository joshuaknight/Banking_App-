



function onload(){
		$("#address_details,#account_details,#customer_details").accordion({
			animate:300,
			active:1,
			collapsible:true,
			event:"click",			
			heightStyle: "content",
		});

		$("#account_type,#joint_account,#gender").selectmenu({
			width:200,			
		});

		$("#age").datepicker({
			changeMonth : true,
			changeYear : true,
			maxDate : -365 * 14,
			minDate : -365 * 100,			
		});

		$(".main_form").tabs({
			event:"click",
			show:"fadeIn",
			hide:"fadeOut",
			active:1,
			collapsible:true,
			heightStyle:"content"
		});

		acc = new Create_account()
		acc.grabbler()
}

onload()
