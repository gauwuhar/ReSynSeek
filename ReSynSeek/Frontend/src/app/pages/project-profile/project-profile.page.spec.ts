import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectProfileComponent } from './project-profile.page';

describe('ProjectProfileComponent', () => {
  let component: ProjectProfileComponent;
  let fixture: ComponentFixture<ProjectProfileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProjectProfileComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProjectProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

});
