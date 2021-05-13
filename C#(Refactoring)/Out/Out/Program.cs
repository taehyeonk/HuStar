using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Out
{
    class Program
    {
        // return을 두 개를 받고 싶을 때 사용하는 것이 out
        static int Sum(out float avg)
        {
            int iSum = 0;
            for (int i = 0; i < 10; i++)
            {
                iSum += i;
            }
            avg = iSum / 10.0f;
            return iSum;
        }
        static void Main(string[] args)
        {
            float avg = 0.0f;
            int iSum = Sum(out avg);
            Console.WriteLine("Sum: {0}, Avg: {1}", iSum, avg);
        }
    }
}
