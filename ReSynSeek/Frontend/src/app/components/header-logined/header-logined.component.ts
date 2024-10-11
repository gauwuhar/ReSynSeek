import { Component } from '@angular/core';

@Component({
  selector: 'app-header-logined',
  standalone: true,
  templateUrl: './header-logined.component.html',
  styleUrls: ['./header-logined.component.sass']
})
export class HeaderLoginedComponent {
  languages: string[] = ["English", "Русский", "Қазақша"];
  selectedLanguage: string = this.languages[0]; // Default language
  dropdownActive: boolean = false;

  get languageOptions() {
    return this.languages.filter(lang => lang !== this.selectedLanguage);
  }

  selectLanguage(language: string): void {
    this.selectedLanguage = language;
    this.dropdownActive = false; // Close dropdown after selection
  }

  toggleDropdown(): void {
    this.dropdownActive = !this.dropdownActive;
  }

  closeDropdown(event: MouseEvent): void {
    const target = event.target as HTMLElement;
    if (!target.closest('.language-selector__dropdown') && !target.closest('#languageToggle')) {
      this.dropdownActive = false;
    }
  }
}
