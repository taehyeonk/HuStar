using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GenericCollection
{
    class Program
    {
        class MyArray<T>
        {
            public MyArray(int iSize = 10)
            {
                m_data = new T[iSize];
            }
            public T this[int iIndex]
            {
                get
                {
                    return m_data[iIndex];
                }
                set
                {
                    m_data[iIndex] = value;
                }
            }
            public int Size()
            {
                return m_data.Length;
            }
            private T[] m_data;
        }
        static void Main(string[] args)
        {
            MyArray<int> intArray = new MyArray<int>();
            for (int i = 0; i < intArray.Size(); i++)
            {
                intArray[i] = i;
                Console.WriteLine("iArray[{0}]: {1}", i, intArray[i]);
            }

            MyArray<float> floatArray = new MyArray<float>();
            for (int i = 0; i < floatArray.Size(); i++)
            {
                floatArray[i] = i * 1.1f;
                Console.WriteLine("iArray[{0}]: {1}", i, floatArray[i]);
            }
        }
    }
}
