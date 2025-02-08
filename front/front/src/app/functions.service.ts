import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class FunctionsService {

  constructor(private http:HttpClient) { }

  showresponse(data:any):Observable<any>{
    return this.http.post(`http://localhost:8000/predict/`,data);
  }
}
