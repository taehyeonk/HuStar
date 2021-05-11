using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VideoManager
{
    class Video
    {
        private string m_Title;
        private string m_Actor;
        private string m_Director;
        private int m_iVideoGubun;

        public void InputData()
        {
            Console.Write("영화제목: ");
            m_Title = Console.ReadLine();
            Console.Write("주연배우: ");
            m_Actor = Console.ReadLine();
            Console.Write("영화감독: ");
            m_Director = Console.ReadLine();
            Console.Write("1. 신규비디오, 2.일반비디오, 3.구비디오: ");
            m_iVideoGubun = int.Parse(Console.ReadLine());
        }

        public void PrintData()
        {
            Console.WriteLine("영화제목 : {0}", m_Title);
            Console.WriteLine("주연배우 : {0}", m_Actor);
            Console.WriteLine("영화감독 : {0}", m_Director);
            Console.Write("비디오 구분: ");
            switch (m_iVideoGubun)
            {
                case 1:
                    Console.WriteLine("신규비디오");
                    break;
                case 2:
                    Console.WriteLine("일반비디오");
                    break;
                case 3:
                    Console.WriteLine("구비디오");
                    break;
            }
            Console.Write("대여료: ");
            switch (m_iVideoGubun)
            {
                case 1:
                    Console.WriteLine("2000");
                    break;
                case 2:
                    Console.WriteLine("1000");
                    break;
                case 3:
                    Console.WriteLine("500");
                    break;
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Video v = new Video();
            v.InputData();
            v.PrintData();
        }
    }
}
