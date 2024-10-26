import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-creating-project-topic',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './creating-project-topic.page.html',
  styleUrls: ['./creating-project-topic.page.sass']
})
export class CreatingProjectTopicPage{
  ngOnInit() {
    const choosePhotoBtn = document.getElementById('choose-photo-btn');
    const fileInput = document.getElementById('file-input') as HTMLInputElement;
    const photoPreview = document.getElementById('photo-preview') as HTMLImageElement;

    // Trigger file input when the 'Choose Photo' button is clicked
    choosePhotoBtn?.addEventListener('click', () => {
      fileInput?.click();
    });

    // Handle file input change to display the image preview
    fileInput?.addEventListener('change', (event: Event) => {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files[0]) {
        const file = target.files[0];
        const reader = new FileReader();

        // Display the selected image as a preview
        reader.onload = (e: ProgressEvent<FileReader>) => {
          if (e.target?.result) {
            photoPreview.src = e.target.result as string;
            photoPreview.style.display = 'block';
          }
        };
        reader.readAsDataURL(file);
      }
    });
  }
  constructor(private router: Router) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        const fragment = this.router.parseUrl(this.router.url).fragment;
        if (fragment) {
          document.getElementById(fragment)?.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  }
}
