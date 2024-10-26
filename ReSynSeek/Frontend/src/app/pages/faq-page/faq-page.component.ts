import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { FAQComponent } from "../FAQ_p/faq/faq.page";
import { FooterComponent } from "../../components/footer/footer.component";

@Component({
  selector: 'app-faq-page',
  standalone: true,
  imports: [HeaderLoginedComponent, FAQComponent, FooterComponent],
  templateUrl: './faq-page.component.html',
  styleUrl: './faq-page.component.sass'
})
export class FaqPageComponent {

}
