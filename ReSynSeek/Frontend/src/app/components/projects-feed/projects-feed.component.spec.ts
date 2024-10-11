import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectsFeedComponent } from './projects-feed.component';

describe('ProjectsFeedComponent', () => {
  let component: ProjectsFeedComponent;
  let fixture: ComponentFixture<ProjectsFeedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProjectsFeedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProjectsFeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
