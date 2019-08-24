using System;
using System.Linq;
namespace BinarySearch
{
    class Program
    {
        static void Main(string[] args)
        {
            while (true)
            {
                try
                {
                    Console.Write("Base : ");
                    int[] Base = Console.ReadLine().Split(' ', ',')
                        .Select(int.Parse).ToArray();
                    Console.Write("Find : ");
                    int Value = int.Parse(Console.ReadLine());
                    int? Result = BinarySearch(Base, Value);
                    if (Result != null) Console.WriteLine("Found, at Base[{0}].", Result);
                    else Console.WriteLine("Not found.");
                }
                catch (Exception e) { break; }
            }
            Console.Write("Press any key to continue...");
            Console.ReadKey(true);
        }
        
        static int? BinarySearch(int[] Base, int Value, int[] Interval = null)
        {
            Interval = Interval ?? new int[] { 0, Base.Length };
            Console.WriteLine("Searching between Base[{0}] and Base[{1}]...",
                Interval[0], Interval[1]);
            if (Interval.Length != 2) throw new ArgumentOutOfRangeException();
            int Middle = (Interval[0] + Interval[1]) / 2;
            if (Base[Middle] == Value) return Middle;
            else if (Interval[0] > Interval[1]) return null;
            else if (Base[Middle] < Value)
                return BinarySearch(Base, Value, new int[] { Middle + 1, Interval[1] });
            else if (Base[Middle] > Value)
                return BinarySearch(Base, Value, new int[] { Interval[0], Middle - 1 });
            else return null;
        }
    }
}
