import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { FooterComponent } from "../../components/footer/footer.component";
import { UserSettingsLookingForComponent } from '../new-project-creation/user-settings-looking-for/user-settings-looking-for.page';

@Component({
  selector: 'app-creating-project-vacancies-page',
  standalone: true,
  imports: [HeaderLoginedComponent, FooterComponent, UserSettingsLookingForComponent],
  templateUrl: './creating-project-vacancies-page.component.html',
  styleUrl: './creating-project-vacancies-page.component.sass'
})
export class CreatingProjectVacanciesPageComponent {

}
