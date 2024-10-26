import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SafetySettingsPageComponent } from './safety-settings-page.component';

describe('SafetySettingsPageComponent', () => {
  let component: SafetySettingsPageComponent;
  let fixture: ComponentFixture<SafetySettingsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SafetySettingsPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SafetySettingsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
