import { BrowserModule, enableDebugTools } from '@angular/platform-browser';
import { NgModule, ApplicationRef } from '@angular/core';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import {MaterialModule} from './material.module';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SidenavResponsiveComponent } from './sidenav-responsive/sidenav-responsive.component';
import { ProjectsSummaryComponent } from './components/projects-summary/projects-summary.component';
import { MessagesComponent } from './components/messages/messages.component';



@NgModule({
  declarations: [
    AppComponent,
    SidenavResponsiveComponent,
    ProjectsSummaryComponent,
    MessagesComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialModule,
    NgbModule.forRoot(),
    BrowserAnimationsModule,
  ],
  providers: [],
  bootstrap: [AppComponent, SidenavResponsiveComponent],
  // entryComponents: []
})
export class AppModule { }
