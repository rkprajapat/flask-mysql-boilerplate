import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectsSummaryComponent } from './projects-summary.component';

describe('ProjectsSummaryComponent', () => {
  let component: ProjectsSummaryComponent;
  let fixture: ComponentFixture<ProjectsSummaryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProjectsSummaryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProjectsSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
