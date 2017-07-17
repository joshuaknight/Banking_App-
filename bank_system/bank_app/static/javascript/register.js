
function Create_account(){
		this.id = null; 

		//account
		this.account_name = null;		
		this.balance = null;
		this.account_type = null;
		this.joint_account = null;

		//customer 
		this.cust_name = null;
		this.cust_phone = null;
		this.cust_age = null;
		this.cust_email = null;		
		this.cust_gender = null;
		
		//Address 
		this.street_no = null;
		this.street_name = null;
		this.addr_district = null;
		this.addr_pincode = null;
		this.addr_state = null;
		this.addr_country = null;				
}


Create_account.prototype.grabbler = function(){
		this.account_name = $("#account_name")[0];
		this.account_type = $("#account_type")[0];
		this.joint_account = $("#joint_account")[0];
		this.cust_name = $("#name")[0];  
		this.cust_phone = $("#phone")[0];  
		this.cust_age = $("#age")[0];  
		this.cust_email = $("#email")[0];  		
		this.cust_gender = $("#gender")[0];
		this.balance = $("#balance")[0];
		this._submit = $("#submit")[0];		
		this.street_no = $("#street_no")[0];
		this.street_name = $("#street_name")[0];
		this.addr_district = $("#addr_district")[0];
		this.addr_pincode = $("#addr_pincode")[0];
		this.addr_state = $("#addr_state")[0];
		this.addr_country = $("#addr_country")[0];		
		var p = this;
		test();
		this.validate();
		$(this._submit).click(function(){
			p.submit();
		});		
}

Create_account.prototype.further_payment = function(){
		$('.main_form')[0].remove('')
		var button = document.createElement('button');
		$(button).addClass("btn btn-success"); 
		$(button).html('Proceed With Payment'); 
		$(".container")[0].append(button);
}

Create_account.prototype.submit = function(){			
		var p = this;

		if (this.validated_true()){									
			var address = this.street_no.value + ' ' +this.street_name.value + ' ' + this.addr_district.value + 
						' '+ this.addr_state.value + ' '+ this.addr_country.value + ' '+this.addr_pincode.value;
			$.ajax({
					url : '/account/add',
					data : {
								account_name : this.account_name.value,
								balance : this.balance.value,
								account_type : this.account_type.value,
								joint_account : this.joint_account.value,
								address : address,
								phone : this.cust_phone.value,
								email : this.cust_email.value,
								name : this.cust_name.value,
								age : this.cust_age.value,
								gender : this.cust_gender.value,							
					},
					type : "POST",
					datatype : "json",			
			}).done(function(json){
					p.further_payment();
			});		
		}
		else{
			alert("Error in Form");
		}
}

Create_account.prototype.test_changed = function(regex,node){				
		if(regex.test(node)){
			return true; 
		}
		else{
			return false; 
		}
}


Create_account.prototype.validate = function(){
		var p = this;
		$("input[type='text']#account_name").val("joshua");
		$(this.account_name).change(function(){			
			
			if (p.test_changed(/^[A-Za-z]{2,15}\s?$/,p.account_name.value)){				
				
				$("#help_text_acname")[0].innerHTML = "";
			}
			else{				
				$("#help_text_acname")[0].innerHTML = "Account Name not valid";
			}
		});
		$(this.balance).change(function(){		
			
			if (p.test_changed(/^[0-9]{3,10}$/,p.balance.value)){							
				
				$("#help_text_balance")[0].innerHTML = "";
			}				
			else{
				$("#help_text_balance")[0].innerHTML = "Invalid Number";
			}
		});
		$(this.account_type).click(function(){	
			
			if (p.account_type.value != 'select'){						
				
				$("#help_text_account_type")[0].innerHTML = "";
			}
			else{
				$("#help_text_account_type")[0].innerHTML = "Account Type not Valid";
			}			
		});
		$(this.joint_account).click(function(){		
			
			if (p.joint_account.value != 'select') {							
				
				$("#help_text_joint_account")[0].innerHTML = "";
			}
			else{
				$("#help_text_joint_account")[0].innerHTML = "No Joint Account Found";
			}						
		});		
		$(this.street_no).change(function(){	
			
			
			if (p.test_changed(/^[0-9]{2,6}$/,p.street_no.value)){
				
				$("#help_text_street_no")[0].innerHTML = "";
			}
			else{
				$("#help_text_street_no")[0].innerHTML = "Street No, not Valid";
			}
		});			
		$(this.street_name).change(function(){	
			
			
			if (p.test_changed(/^[a-zA-Z]{2,12}\s?([a-zA-Z]{2,12})?\s?$/,p.street_name.value)){
			
				$("#help_text_street_name")[0].innerHTML = "";
			}
			else{
				$("#help_text_street_name")[0].innerHTML = "Street Name, not Valid";
			}
		});		

		$(this.addr_district).change(function(){	
			
			
			if (p.test_changed(/^[a-zA-Z]{2,12}\s?$/,p.addr_district.value)){
			
				$("#help_text_district")[0].innerHTML = "";
			}
			else{
				$("#help_text_district")[0].innerHTML = "District Name not Valid";
			}
		});		

		$(this.addr_pincode).change(function(){	
			
			
			if (p.test_changed(/^[0-9]{6}\s?$/,p.addr_pincode.value)){
			
				$("#help_text_pincode")[0].innerHTML = "";
			}
			else{
				$("#help_text_pincode")[0].innerHTML = "Pincode not Valid";
			}
		});			


		$(this.addr_state).change(function(){	
						
			if (p.test_changed(/^[a-zA-Z]{2,20}\s?([a-zA-z]{1,20})?\s?$/,p.addr_state.value)){
			
				$("#help_text_state")[0].innerHTML = "";
			}
			else{
				$("#help_text_state")[0].innerHTML = "State Name not Valid";
			}
		});	

		$(this.addr_country).change(function(){				
			
			if (p.test_changed(/^[a-zA-Z]{2,20}\s?([a-zA-z]{1,20})?\s?$/,p.addr_country.value)){			
				$("#help_text_country")[0].innerHTML = "";
			}
			else{
				$("#help_text_country")[0].innerHTML = "Country Name not Valid";
			}
		});	

		$(this.cust_phone).change(function(){			
			
			if (p.test_changed(/^[9]?[1]?[0-9]{10}\s?$/,p.cust_phone.value)) {				

				$("#help_text_phone")[0].innerHTML = "";
			}
			else{
				$("#help_text_phone")[0].innerHTML = "Phone Number Not Valid";
			}						
		});		


		$(this.cust_email).change(function(){	

			if (p.test_changed(/^[a-zA-Z][._\w]+@([a-z]{2,20})?[a-z.A-Z]{2,20}\.[a-z]{2,3}$/,p.cust_email.value)) {				

				$("#help_text_email")[0].innerHTML = "";
			}
			else{
				$("#help_text_email")[0].innerHTML = "Email Name not valid";
			}							
		});						
		$(this.cust_name).change(function(){

			if (p.test_changed(/^[a-zA-Z]{1}\.[a-z]{3,10}$/,p.cust_name.value)) {

				$("#help_text_name")[0].innerHTML = "";
			}
			else{
				$("#help_text_name")[0].innerHTML = "Name can only contain alphabets";
			}								
		});			

		$(this.cust_age).change(function(){			

			if (p.test_changed(/^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}$/,p.cust_age.value)) {				

				$("#help_text_age")[0].innerHTML = "";
			}
			else{
				$("#help_text_age")[0].innerHTML = "Age must be above 18 and only in integers";
			}						
		});			

		$(this.cust_gender).click(function(){	

			if (p.cust_gender.value != 'select') {				
				
				$("#help_text_gender")[0].innerHTML = "";											
			}
			else{
				$("#help_text_gender")[0].innerHTML = "Select Either Male or Female";
			}											
		});

}


Create_account.prototype.validated_true = function(){
		var p = this;		
		if (
				(p.test_changed(/^[A-Za-z]{2,15}\s?$/,p.account_name.value)) &&
				(p.test_changed(/^[0-9]{3,10}$/,p.balance.value)) &&
				(p.account_type.value != 'select') &&
				(p.joint_account.value != 'select') &&
				(p.test_changed(/^[0-9]{2,6}$/,p.street_no.value)) &&
				(p.test_changed(/^[a-zA-Z]{2,12}\s?([a-zA-Z]{2,12})?\s?$/,p.street_name.value)) &&
				(p.test_changed(/^[a-zA-Z]{2,12}\s?$/,p.addr_district.value)) && 
				(p.test_changed(/^[0-9]{6}\s?$/,p.addr_pincode.value)) &&
				(p.test_changed(/^[a-zA-Z]{2,20}\s?([a-zA-z]{1,20})?\s?$/,p.addr_state.value)) &&
				(p.test_changed(/^[a-zA-Z]{2,20}\s?([a-zA-z]{1,20})?\s?$/,p.addr_country.value)) &&
				(p.test_changed(/^[9]?[1]?[0-9]{10}\s?$/,p.cust_phone.value)) &&
				(p.test_changed(/^[a-zA-Z][._\w]+@([a-z]{2,20})?[a-z.A-Z]{2,20}\.[a-z]{2,3}$/,p.cust_email.value)) &&
				(p.test_changed(/^[a-zA-Z]{1}\.[a-z]{3,10}$/,p.cust_name.value)) &&
				(p.test_changed(/^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}$/,p.cust_age.value)) &&
				(p.cust_gender.value != 'select') 
			)
				return true;			
		else{
				return false;
		}		
}

