import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatingProjectTopicPageComponent } from './creating-project-topic-page.component';

describe('CreatingProjectTopicPageComponent', () => {
  let component: CreatingProjectTopicPageComponent;
  let fixture: ComponentFixture<CreatingProjectTopicPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreatingProjectTopicPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreatingProjectTopicPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
