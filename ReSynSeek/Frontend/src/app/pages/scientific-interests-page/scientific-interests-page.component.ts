import { Component } from '@angular/core';
import { HeaderComponent } from "../../components/header/header.component";
import { ScientificInterestsPage } from '../scientific-interests/scientific-interests.page';
import { FooterComponent } from "../../components/footer/footer.component";

@Component({
  selector: 'app-scientific-interests-page',
  standalone: true,
  imports: [HeaderComponent, ScientificInterestsPage, FooterComponent],
  templateUrl: './scientific-interests-page.component.html',
  styleUrl: './scientific-interests-page.component.sass'
})
export class ScientificInterestsPageComponent {

}
