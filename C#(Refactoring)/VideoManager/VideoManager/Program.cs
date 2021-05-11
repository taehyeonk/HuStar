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

        public virtual VideoGubun Up()
        {
            return null;
        }

        public virtual VideoGubun Down()
        {
            return null;
        }
    }

    class NewVideo : VideoGubun
    {
        private static VideoGubun m_VideoGubun = null;
        private NewVideo() { }

        public static VideoGubun CreateVideoGubun()
        {
            if(m_VideoGubun == null)
            {
                m_VideoGubun = new NewVideo();
            }
            return m_VideoGubun;
        }

        public override string GetVideoGubun()
        {
            return "신규비디오";
        }

        public override int GetRentalPrice()
        {
            return 2000;
        }

        public override VideoGubun Up()
        {
            return this;
        }

        public override VideoGubun Down()
        {
            return NormalVideo.CreateVideoGubun();
        }
    }

    class NormalVideo : VideoGubun
    {
        private static VideoGubun m_VideoGubun = null;
        private NormalVideo() { }

        public static VideoGubun CreateVideoGubun()
        {
            if (m_VideoGubun == null)
            {
                m_VideoGubun = new NormalVideo();
            }
            return m_VideoGubun;
        }

        public override string GetVideoGubun()
        {
            return "일반비디오";
        }

        public override int GetRentalPrice()
        {
            return 1000;
        }

        public override VideoGubun Up()
        {
            return NewVideo.CreateVideoGubun();
        }

        public override VideoGubun Down()
        {
            return OldVideo.CreateVideoGubun();
        }
    }

    class OldVideo : VideoGubun
    {
        private static VideoGubun m_VideoGubun = null;
        private OldVideo() { }

        public static VideoGubun CreateVideoGubun()
        {
            if (m_VideoGubun == null)
            {
                m_VideoGubun = new OldVideo();
            }
            return m_VideoGubun;
        }

        public override string GetVideoGubun()
        {
            return "구비디오";
        }

        public override int GetRentalPrice()
        {
            return 500;
        }

        public override VideoGubun Up()
        {
            return NormalVideo.CreateVideoGubun();
        }

        public override VideoGubun Down()
        {
            return this;
        }
    }

    class VideoGubunInputBase
    {
        protected List<VideoGubun> m_VideoGubunList = new List<VideoGubun>();

        public VideoGubunInputBase() // 생성자
        {
            m_VideoGubunList.Add(NormalVideo.CreateVideoGubun());
            m_VideoGubunList.Add(NewVideo.CreateVideoGubun());
            m_VideoGubunList.Add(OldVideo.CreateVideoGubun());
        }

        public virtual void DisplayMenu() { }

        public VideoGubun GetVideoGubun()
        {
            DisplayMenu();
            int iVideoGubun = int.Parse(Console.ReadLine());
            return m_VideoGubunList[iVideoGubun - 1]; // list의 index는 0부터 시작하므로 -1 해줌
        }
    }

    class VideoGubunInputRow : VideoGubunInputBase
    {
        public override void DisplayMenu()
        {
            for(int i=0; i<m_VideoGubunList.Count; i++)
            {
                Console.WriteLine("{0}.{1}", i + 1, m_VideoGubunList[i].GetVideoGubun());
            }
        }
    }

    class VideoGubunInputCol: VideoGubunInputBase
    {
        public override void DisplayMenu()
        {
            for (int i = 0; i < m_VideoGubunList.Count; i++)
            {
                Console.Write("{0}.{1} ", i + 1, m_VideoGubunList[i].GetVideoGubun());
            }
        }
    }

    class Video
    {
        private string m_Title;
        private string m_Actor;
        private string m_Director;
        private VideoGubun m_VideoGubun;

        public void InputData(VideoGubunInputBase vInput)
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

        public void UpVideoGubun()
        {
            m_VideoGubun = m_VideoGubun.Up();
        }

        public void DownVideoGubun()
        {
            m_VideoGubun = m_VideoGubun.Down();
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Video v = new Video();
            VideoGubunInputBase vInput = new VideoGubunInputRow();
            v.InputData(vInput);
            v.PrintData();
            v.UpVideoGubun();
            v.PrintData();
            v.DownVideoGubun();
            v.PrintData();
            v.DownVideoGubun();
            v.PrintData();
        }
    }
}