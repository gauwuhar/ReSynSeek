import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { ProjectProfileComponent } from "../project-profile/project-profile.page";
import { FooterComponent } from "../../components/footer/footer.component";

@Component({
  selector: 'app-project-profile-page',
  standalone: true,
  imports: [HeaderLoginedComponent, ProjectProfileComponent, FooterComponent],
  templateUrl: './project-profile-page.component.html',
  styleUrl: './project-profile-page.component.sass'
})
export class ProjectProfilePageComponent {

}
