using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using opennlp.tools.ngram;

namespace makeData
{
    class Program
    {
        public static List<string> stop = new List<string>();
        public static List<int[]> tweetsFinal = new List<int[]>();

        static void leerStopWords()
        {
            string path = @"./data/stop.txt";
            HashSet<string> types = new HashSet<string>();

            using (StreamReader sr = new StreamReader(path))
            {
                while (sr.Peek() >= 0)
                {
                    stop.Add(sr.ReadLine());
                }
            }
        }

        static string quitarStopWords(string token)
        {
            foreach (var item in stop)
            {
                token.Replace(item, "");
            }

            return token;
        }
        static void Main(string[] args)
        {
            //Leer archivo
            string path = @"./data/";
            string inputData = "corpusTweets.csv";
            string exitData = "corpusTweetsCaracterizado.csv";

            HashSet<string> types = new HashSet<string>();
            leerStopWords();

            //crear vocabulario
            using (StreamReader sr = new StreamReader(path+inputData))
            {
                while (sr.Peek() >= 0)
                {
                    string line = sr.ReadLine();
                    string[] lineArray = line.Split(',');

                    if (!(lineArray.Length < 3))
                    {
                        //descartamos tuits tipo 3
                        if (lineArray[1] != "3")
                        {
                            if ((lineArray[1] != "" && lineArray[2] != ""))
                            {
                                string tweet = lineArray[0];
                                //tweet.Replace("|", ""); //quitar comas
                                tweet.Replace("|", ","); //regresar comas
                                tweet = quitarStopWords(tweet); //quitar stops words
                                tweet = tweet.ToLower(); //minusculas

                                var ngrams = NGramGenerator.generate(tweet.ToArray(), 3, "");//creamos trigramas
                                dynamic ngramsArray = ngrams.toArray();

                                foreach (var token in ngramsArray)
                                {
                                    types.Add(token);
                                }
                            }
                        }
                    }
                }
            }

            //caracterizar tweets
            using (StreamReader sr = new StreamReader(path+inputData))
            {
                while (sr.Peek() >= 0)
                {
                    string line = sr.ReadLine();
                    string[] lineArray = line.Split(',');

                    if (!(lineArray.Length < 3))
                    {
                        //descartamos tuits tipo 3
                        if (lineArray[1] != "3")
                        {
                            if ((lineArray[1] !="" && lineArray[2]!=""))
                            {

                                string tweet = lineArray[0];
                                //tweet.Replace("|", ""); //quitar comas
                                tweet.Replace("|", ","); //regresar comas
                                tweet = quitarStopWords(tweet); //quitar stops words
                                tweet = tweet.ToLower(); //minusculas

                                var ngrams = NGramGenerator.generate(tweet.ToArray(), 3, "");//creamos trigramas
                                dynamic ngramsArray = ngrams.toArray();

                                int[] tweetCaract = new int[types.Count];
                                Array.Clear(tweetCaract, 0, tweetCaract.Length);

                                int count = 0;
                                //for (int i = 0; i < types.Count; i++)
                                foreach (var item in types)
                                {
                                    for (int j = 0; j < ngramsArray.Length; j++)
                                    {
                                        if (item == ngramsArray[j])
                                        {
                                            tweetCaract[count] = 1;
                                        }
                                    }
                                    count++;
                                }

                                //tweetsFinal.Add(tweetCaract);
                                //escribir en archivo
                                int target;
                                if (lineArray[2] == "amlo")
                                {
                                    target = 0;
                                }
                                else if (lineArray[2] == "anaya")
                                {
                                    target = 1;
                                }
                                else if (lineArray[2] == "meade")
                                {
                                    target = 2;
                                }
                                else if (lineArray[2] == "bronco")
                                {
                                    target = 3;
                                }
                                else if (lineArray[2] == "debate")
                                {
                                    target = 4;
                                }
                                else
                                {
                                    target = 5;
                                }


                                using (TextWriter tw = new StreamWriter(path + exitData, true))
                                {
                                    for (int i = 0; i < tweetCaract.Length; i++)
                                    {
                                        tw.Write(tweetCaract[i]);
                                    }
                                    tw.Write(" " + lineArray[1]);
                                    tw.WriteLine();
                                }

                            }
                        }
                    }
                }
            }
        }
    }
}
