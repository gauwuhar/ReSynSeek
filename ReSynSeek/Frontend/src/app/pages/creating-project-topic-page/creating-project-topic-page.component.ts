import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { HeaderComponent } from "../../components/header/header.component";
import { CreatingProjectTopicPage } from "../creating-project-topic/creating-project-topic.page";
import { FooterComponent } from "../../components/footer/footer.component";

@Component({
  selector: 'app-creating-project-topic-page',
  standalone: true,
  imports: [HeaderLoginedComponent, HeaderComponent, CreatingProjectTopicPage, FooterComponent],
  templateUrl: './creating-project-topic-page.component.html',
  styleUrl: './creating-project-topic-page.component.sass'
})
export class CreatingProjectTopicPageComponent {

}
