import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http: HttpClient) { }

  postHashtag(hash: string) {
    this.http.get(`http://localhost:5000/api/v1/tweets/${hash}`).subscribe(result => {
      console.log(result);
    }, error => {
      console.log(error.error);
    });
  }
}
