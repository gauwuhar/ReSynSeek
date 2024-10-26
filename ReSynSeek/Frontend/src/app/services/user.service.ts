import { Injectable } from '@angular/core';
import { SubjectModel } from "../model/subject-model";
import { AboutMeModel } from "../model/about-me.model";

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor() { }

  getScientificInterests(): SubjectModel[] {
    return [
      {
        id: '1',
        title: 'Project Management',
        url: '/assets/Project_Management.jpg'
      },
      {
        id: '2',
        title: 'Applied data analytics',
        url: '/assets/Applied_data_analytics.jpg'
      },
      {
        id: '3',
        title: 'Digital public administration',
        url: '/assets/Digital_public_administration.jpg'
      },
      {
        id: '4',
        title: 'Computer Science',
        url: '/assets/Computer_Science.jpg'
      },
      {
        id: '5',
        title: 'Software Engineering',
        url: '/assets/Software_Engineering.jpg'
      },
      {
        id: '6',
        title: 'Big Data Analysis',
        url: '/assets/Big_Data_Analysis.jpg'
      },
      {
        id: '7',
        title: 'Media Technologies',
        url: '/assets/Media_Technologies.jpg'
      },
      {
        id: '8',
        title: 'Mathematical and Computational Science',
        url: '/assets/Mathematical_and_Computational_Science.jpg'
      },
      {
        id: '9',
        title: 'Big Data in Healthcare',
        url: '/assets/Big_Data_in_Healthcare.jpg'
      },
      {
        id: '10',
        title: 'Cybersecurity',
        url: '/assets/Cybersecurity.jpg'
      },
      {
        id: '11',
        title: 'Smart Technologies',
        url: '/assets/Smart_Technologies.jpg'
      },
      {
        id: '12',
        title: 'Industrial Internet of Things',
        url: '/assets/Industrial_Internet_of_Things.jpg'
      },
      {
        id: '13',
        title: 'Electronic Engineering',
        url: '/assets/Electronic_Engineering.jpg'
      },
      {
        id: '14',
        title: 'IT Management',
        url: '/assets/IT_Management.jpg'
      },
      {
        id: '15',
        title: 'IT Entrepreneurship',
        url: '/assets/IT_Entrepreneurship.jpg'
      },
      {
        id: '16',
        title: 'AI Business',
        url: '/assets/AI_Business.jpg'
      },
      {
        id: '17',
        title: 'Digital Journalism',
        url: '/assets/Digital_Journalism.jpg'
      },
      {
        id: '18',
        title: 'Computer Science and Information Networks',
        url: '/assets/Computer_Scienc_and_Information_Networks.jpg'
      },
    ];
  };

  getAboutMe(): AboutMeModel {
    return {
      aboutMe: "Just a regular human trying to convince AI that I'm not a robot. Successfully aced CAPTCHA 10 times in a row.",
      scientificExperience: [
        "Master of turning coffee into code (self-proclaimed)",
        "Co-Founder of the 'Procrastinators Anonymous' club (we'll have our first meeting... eventually)",
        "Once debugged a program with sheer willpower and questionable keyboard smashing"
      ],
      working: ["Currently pretending to be productive while actually Googling 'funny coding memes'", 'asdasdasdasd some shit'],
      edSkills: ["Expert in pushing buttons and hoping something magical happens. Also, I can kind of code."],
      contacts: ["Carrier pigeon, smoke signals, or @funnycoder if you're tech-savvy."],
    }
  }
}
