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
        title: 'Psychology',
        url: 'https://www.recordnet.com/gcdn/presto/2021/03/22/NRCD/9d9dd9e4-e84a-402e-ba8f-daa659e6e6c5-PhotoWord_003.JPG'
      },
      {
        id: '2',
        title: 'Minecraft',
        url: 'https://www.minecraft.net/content/dam/games/minecraft/key-art/Vanilla-PMP_Collection-Carousel-0_Buzzy-Bees_1280x768.jpg'
      },
      {
        id: '3',
        title: 'Gachi',
        url: 'https://i1.sndcdn.com/avatars-YxyX81sc0yxz8UN5-49eERw-t240x240.jpg'
      },
      {
        id: '4',
        title: 'Linkin Park',
        url: 'https://townsquare.media/site/366/files/2014/12/Linkin-Park.jpg?w=780&q=75'
      },
      {
        id: '5',
        title: 'Anime',
        url: 'https://m.media-amazon.com/images/S/pv-target-images/c912a1ce1d58e50f37495f640cb61839c7183adb78470593267cabaedf4fd3c8._SX1080_FMjpg_.jpg'
      },
      {
        id: '6',
        title: 'Dota 2',
        url: 'https://pikuco.ru/upload/test_stable/406/406d7ecf04c78ac496a3efdf04a353b7.webp'
      },
      {
        id: '7',
        title: 'Україна',
        url: 'https://ichef.bbci.co.uk/news/976/cpsprodpb/1601E/production/_109224109_ukraine.png'
      },
      {
        id: '8',
        title: 'AITU',
        url: 'https://astanait.edu.kz/wp-content/uploads/2020/11/DSC01501-scaled.jpg'
      },
      {
        id: '8',
        title: 'The United States of America',
        url: 'https://i.natgeofe.com/k/57873055-5e16-4eac-add4-c08c8b5f3bd7/united-states-statue-of-liberty_square.jpg'
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
