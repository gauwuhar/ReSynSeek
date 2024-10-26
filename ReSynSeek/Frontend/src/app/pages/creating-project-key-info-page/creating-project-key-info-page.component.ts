import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { FooterComponent } from "../../components/footer/footer.component";
import { CreatingProjectKeyInfoPage } from '../creating-project-key-info/creating-project-key-info.page';

@Component({
  selector: 'app-creating-project-key-info-page',
  standalone: true,
  imports: [HeaderLoginedComponent, FooterComponent, CreatingProjectKeyInfoPage],
  templateUrl: './creating-project-key-info-page.component.html',
  styleUrl: './creating-project-key-info-page.component.sass'
})
export class CreatingProjectKeyInfoPageComponent {

}
