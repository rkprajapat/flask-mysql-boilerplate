import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ProjectsSummaryComponent } from './components/projects-summary/projects-summary.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: '/',
    pathMatch: 'full'
  },
  {
    path: 'instance',
    component: ProjectsSummaryComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes,
    // { enableTracing: true }, // <-- debugging purposes only
    // {useHash: true}
  )],
  exports: [RouterModule]
})
export class AppRoutingModule { }
