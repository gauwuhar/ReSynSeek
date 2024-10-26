import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatingProjectTopicPage } from './creating-project-topic.page';

describe('CreatingProjectTopicPage', () => {
  let component: CreatingProjectTopicPage;
  let fixture: ComponentFixture<CreatingProjectTopicPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreatingProjectTopicPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreatingProjectTopicPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
