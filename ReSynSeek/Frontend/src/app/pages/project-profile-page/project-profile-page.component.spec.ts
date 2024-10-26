import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectProfilePageComponent } from './project-profile-page.component';

describe('ProjectProfilePageComponent', () => {
  let component: ProjectProfilePageComponent;
  let fixture: ComponentFixture<ProjectProfilePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProjectProfilePageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProjectProfilePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
