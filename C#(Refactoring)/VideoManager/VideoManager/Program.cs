using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VideoManager
{
    class VideoGubun
    {
        public virtual string GetVideoGubun()
        {
            return "";
        }

        public virtual int GetRentalPrice()
        {
            return 0;
        }
    }

    class NewVideo : VideoGubun
    {
        public override string GetVideoGubun()
        {
            return "신규비디오";
        }

        public override int GetRentalPrice()
        {
            return 2000;
        }
    }

    class NormalVideo : VideoGubun
    {
        public override string GetVideoGubun()
        {
            return "일반비디오";
        }

        public override int GetRentalPrice()
        {
            return 1000;
        }
    }

    class OldVideo : VideoGubun
    {
        public override string GetVideoGubun()
        {
            return "구비디오";
        }

        public override int GetRentalPrice()
        {
            return 500;
        }
    }

    class VideoGubunInput // 변화될 가능성이 많은 부분의 코드는 따로 클래스로 만듦
    {
        public VideoGubun GetVideoGubun()
        {
            Console.Write("1. 신규비디오, 2.일반비디오, 3.구비디오: ");
            int iVideoGubun = int.Parse(Console.ReadLine());
            switch (iVideoGubun)
            {
                case 1:
                    return new NewVideo();
                case 2:
                    return new NormalVideo();
                case 3:
                    return new OldVideo();
                default:
                    return new NewVideo();
            }
        }
    }

    class Video
    {
        private string m_Title;
        private string m_Actor;
        private string m_Director;
        private VideoGubun m_VideoGubun;

        public void InputData(VideoGubunInput vInput)
        {
            Console.Write("영화제목: ");
            m_Title = Console.ReadLine();
            Console.Write("주연배우: ");
            m_Actor = Console.ReadLine();
            Console.Write("영화감독: ");
            m_Director = Console.ReadLine();
            m_VideoGubun = vInput.GetVideoGubun();
        }

        public void PrintData()
        {
            Console.WriteLine("영화제목 : {0}", m_Title);
            Console.WriteLine("주연배우 : {0}", m_Actor);
            Console.WriteLine("영화감독 : {0}", m_Director);
            Console.WriteLine("비디오 구분: {0}", m_VideoGubun.GetVideoGubun());
            Console.WriteLine("대여료: {0}", m_VideoGubun.GetRentalPrice());
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Video v = new Video();
            VideoGubunInput vInput = new VideoGubunInput();
            v.InputData(vInput);
            v.PrintData();
        }
    }
}