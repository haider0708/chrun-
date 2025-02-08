import { Component } from '@angular/core';
import { FunctionsService } from './functions.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: [
    './app.component.css',
    './css/spectre.css',
    './css/yeo.css',
    './css/spectre-icons.css',
    './css/spectre-exp.css',
  ]
  
  
})
export class AppComponent {
  constructor(private user: FunctionsService) {}
  title = 'front';
  State: string = '';
  Total_charge: number = 0;
  Area_code: number = 0;
  Customer_service_calls: number = 0;
  Total_intl_calls: number = 0;
  International_plan: number = 0;
  Number_vmail_messages: number = 0;
  Total_intl_charge: number = 0;
  CScalls_Rate: number = 0;

data: any;

fonc() {
  this.data = {
    State: this.State,
    Total_charge: this.Total_charge,
    Area_code: this.Area_code,
    Customer_service_calls: this.Customer_service_calls,
    Total_intl_calls: this.Total_intl_calls,
    International_plan: this.International_plan,
    Number_vmail_messages: this.Number_vmail_messages,
    Total_intl_charge: this.Total_intl_charge,
    CScalls_Rate: this.CScalls_Rate,
  };
    console.log(this.data);
    this.user.showresponse(this.data).subscribe({
      next: (res) => {
        if(res.prediction==1){
          Swal.fire('Prediction: Client Will churn'); 
        }
        else{
          Swal.fire('Prediction: Client Will NOT churn'); 
        }
        
      },
      error: (err) => {
        alert('Error: ' + err);
      },
    });
  }
}
