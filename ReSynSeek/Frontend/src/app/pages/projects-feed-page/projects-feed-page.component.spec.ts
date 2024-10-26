import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectsFeedPageComponent } from './projects-feed-page.component';

describe('ProjectsFeedPageComponent', () => {
  let component: ProjectsFeedPageComponent;
  let fixture: ComponentFixture<ProjectsFeedPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProjectsFeedPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProjectsFeedPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
