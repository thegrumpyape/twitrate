import { Component, OnInit } from '@angular/core';
import { DataService } from 'src/app/services/data.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  submitValue: string;

  constructor(private dataService: DataService) { }

  ngOnInit() {
  }

  submitHashtag() {
    if (this.submitValue && this.submitValue !== '') {
      this.dataService.postHashtag(this.submitValue);
    }
  }

}
