import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { NewProjectSubmitComponent } from "../new-project-creation/new-project-submit/new-project-submit.page";
import { FooterComponent } from '../../components/footer/footer.component';

@Component({
  selector: 'app-creating-project-submit-page',
  standalone: true,
  imports: [HeaderLoginedComponent, NewProjectSubmitComponent, FooterComponent],
  templateUrl: './creating-project-submit-page.component.html',
  styleUrl: './creating-project-submit-page.component.sass'
})
export class CreatingProjectSubmitPageComponent {

}
