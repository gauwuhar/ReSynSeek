  import { Component, ElementRef, Renderer2, ViewChild } from '@angular/core';
  import { RouterModule } from '@angular/router';

  @Component({
    selector: 'app-creating-project-key-info',
    standalone: true,
    imports: [RouterModule],
    templateUrl: './creating-project-key-info.page.html',
    styleUrls: ['./creating-project-key-info.page.sass']
  })
  export class CreatingProjectKeyInfoPage{

    @ViewChild('buttonContainer') buttonContainer!: ElementRef;

    constructor(private renderer: Renderer2) {}

    toggleButton(button: EventTarget | null): void {
      // Ensure that button is an HTMLElement
      const buttonElement = button as HTMLElement;

      // Toggle the active class
      buttonElement.classList.toggle('active');

      // Find the close button if it exists
      let closeButton = buttonElement.querySelector('.close-btn') as HTMLButtonElement | null;

      if (buttonElement.classList.contains('active')) {
        // If active and close button doesn't exist, create it
        if (!closeButton) {
          closeButton = this.renderer.createElement('button') as HTMLButtonElement;
          closeButton.innerHTML = '✖';
          closeButton.className = 'close-btn';

          // Apply CSS styles directly to the button element
          this.renderer.setStyle(closeButton, 'background-color', '#363940');
          this.renderer.setStyle(closeButton, 'color', '#DCDCDC');
          this.renderer.setStyle(closeButton, 'border', 'none');
          this.renderer.setStyle(closeButton, 'cursor', 'pointer');
          this.renderer.setStyle(closeButton, 'font-size', '12px');

          // Add functionality to remove the main button using addEventListener
          this.renderer.listen(closeButton, 'click', () => {
            buttonElement.remove();
          });

          // Append the close button to the main button
          this.renderer.appendChild(buttonElement, closeButton);
        }
      } else {
        // If deactivated, remove the close button
        if (closeButton) {
          closeButton.remove();
        }
      }
    }

    deleteAllButtons(): void {
      // Get the container with buttons
      const buttonContainer = this.buttonContainer.nativeElement;

      // Remove all buttons inside the container except the "Delete All" button
      buttonContainer.querySelectorAll('.creating-project__keywords-section__keyword-button').forEach((button: HTMLElement) => {
        button.remove();
      });
    }
  }
