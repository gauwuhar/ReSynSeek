import { Component, OnInit } from '@angular/core';
import { SubjectModel } from "../../model/subject-model";
import { NgClass, NgOptimizedImage, NgStyle } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { UserService } from "../../services/user.service";

interface InnerSubjectModel extends SubjectModel {
  selected?: boolean,
}

@Component({
  selector: 'app-scientific-interests.page',
  standalone: true,
  imports: [
    NgOptimizedImage,
    FormsModule,
    NgStyle,
    NgClass
  ],
  templateUrl: './scientific-interests.page.html',
  styleUrl: './scientific-interests.page.sass'
})
export class ScientificInterestsPage implements OnInit {
  subjects: InnerSubjectModel[] = [];

  constructor(
    private userService: UserService,
  ) {
  }

  ngOnInit() {
    this.subjects = this.userService.getScientificInterests().map(s => (
      {
        ...s,
        selected: false,
      }
    ));
    this.subjects = this.userService.getScientificInterests();
  }

  toggleSelected(subject: InnerSubjectModel) {
    subject.selected = !subject.selected;
  }
}
