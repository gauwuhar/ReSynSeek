import { Component } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.sass']
})
export class HeaderComponent {
  isLogin = false;
  languages: { [key: string]: string } = {
    "English": "assets/icons/english-flag.png",
    "Русский": "assets/icons/russian-flag.png",
    "Қазақша": "assets/icons/kazakh-flag.svg"
  };

  selectedLanguage: string = 'English';
  dropdownOpen: boolean = false;

  toggleDropdown(): void {
    this.dropdownOpen = !this.dropdownOpen;
  }

  selectLanguage(language: string): void {
    this.selectedLanguage = language;
    this.dropdownOpen = false;
  }

  get availableLanguages(): string[] {
    return Object.keys(this.languages).filter(lang => lang !== this.selectedLanguage);
  }

  // Handle clicks outside the dropdown to close it
  onClickOutside(event: MouseEvent): void {
    const dropdown = document.querySelector('.language-selector__dropdown') as HTMLElement;
    const languageToggle = document.getElementById('languageToggle') as HTMLElement;
    
    if (dropdown && !dropdown.contains(event.target as Node) && !languageToggle.contains(event.target as Node)) {
      this.dropdownOpen = false;
    }
}
}
