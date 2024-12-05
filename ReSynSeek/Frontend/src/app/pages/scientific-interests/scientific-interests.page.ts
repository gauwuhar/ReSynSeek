import { Component, OnInit } from '@angular/core';
import { SubjectModel } from "../../model/subject-model";
import { FormsModule } from "@angular/forms";
import { NgClass, NgOptimizedImage, NgStyle } from "@angular/common";
import { UserService } from "../../services/user.service";
import { CommonModule } from '@angular/common';

interface InnerSubjectModel extends SubjectModel {
  selected?: boolean;
}

@Component({
  selector: 'app-scientific-interests',
  standalone: true,
  imports: [
    NgOptimizedImage,
    FormsModule,
    NgStyle,
    NgClass,
    CommonModule  // Добавьте это, если используется standalone
  ],
  templateUrl: './scientific-interests.page.html',
  styleUrls: ['./scientific-interests.page.sass']
})
export class ScientificInterestsPage implements OnInit {
  subjects: InnerSubjectModel[] = [];

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.subjects = this.userService.getScientificInterests().map(subject => ({
      ...subject,
      selected: false // Убедитесь, что вы добавляете свойство selected
    }));
  }

  saveInterests() {
    const selectedInterests = this.subjects
      .filter(subject => subject.selected)
      .map(subject => subject.id); // Получите ID выбранных интересов

    this.userService.saveInterests(selectedInterests).subscribe(response => {
      // Обработка ответа от сервера, например, уведомление об успехе
      console.log('Interests saved successfully!', response);
    }, error => {
      // Обработка ошибок
      console.error('Error saving interests', error);
    });
  }


  toggleSelected(subject: InnerSubjectModel) {
    subject.selected = !subject.selected;
  }

  // Track function for better performance with *ngFor
  trackById(index: number, item: InnerSubjectModel): number {
    return typeof item.id === 'number' ? item.id : index;
  }
}
// export class ScientificInterestsPage {

// }
