import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { CongratulationsPopupComponent } from "../../components/congratulations-popup/congratulations-popup.component";
import { ProjectsFeedComponent } from "../projects-feed/projects-feed.page";
import { FooterComponent } from "../../components/footer/footer.component";

@Component({
  selector: 'app-projects-feed-page',
  standalone: true,
  imports: [HeaderLoginedComponent, CongratulationsPopupComponent, ProjectsFeedComponent, FooterComponent],
  templateUrl: './projects-feed-page.component.html',
  styleUrl: './projects-feed-page.component.sass'
})
export class ProjectsFeedPageComponent {

}
