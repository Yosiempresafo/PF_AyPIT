using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace json2tweets
{
    class Program
    {
        static void Main(string[] args)
        {
            int count = 0;
            dynamic stuff = JsonConvert.DeserializeObject("{ 'Name': 'Jon Smith', 'Address': { 'City': 'New York', 'State': 'NY' }, 'Age': 42 }");

            string name = stuff.Name;
            string address = stuff.Address.City;

            string path = @"C:\Users\llara\Google Drive\FI\Octavo semestre\AyPIT\TwitterSA\tweets.json";
            string pathExit = @"C:\Users\llara\Google Drive\FI\Octavo semestre\AyPIT\TwitterSA\corpusTweets.csv";

            StreamWriter sw = new StreamWriter(pathExit, false);
            using (StreamReader sr = new StreamReader(path))
            {
                sw.WriteLine("tweet,sentimiento,target");

                while (sr.Peek() >= 0)
                {
                    //extended_tweet -> full_text
                    dynamic line = JsonConvert.DeserializeObject(sr.ReadLine());

                    string tweet = line.extended_tweet != null?line.extended_tweet.full_text : line.text;
                    tweet = tweet.Replace("\n", " ");
                    tweet = tweet.Replace("#", "");
                    tweet = tweet.Replace("…", "");
                    tweet = tweet.Replace("...", "");
                    tweet = tweet.Replace(",", "|");

                    string tweetReplacePoliticosPepe = Regex.Replace(tweet, @"@JoseAMeadeK", "LUDORULESJoseAMeadeK");
                    string tweetReplacePoliticosAmlo = Regex.Replace(tweetReplacePoliticosPepe, @"@lopezobrador_", "LUDORULESlopezobrador_");
                    string tweetReplacePoliticosBronco = Regex.Replace(tweetReplacePoliticosAmlo, @"@JaimeRdzNL", "LUDORULESJaimeRdzNL");
                    string tweetReplacePoliticosAnaya = Regex.Replace(tweetReplacePoliticosBronco, @"@RicardoAnayaC", "LUDORULESRicardoAnayaC");

                    string tweetReplacePoliticos = Regex.Replace(tweetReplacePoliticosAnaya, @"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)", "");

                    string tweetSinUrl = Regex.Replace(tweetReplacePoliticos, @"http[^\s]+", "");
                    tweetSinUrl = tweetSinUrl.Replace("LUDORULES", "");
                    if (count%12==0)
                    {
                        sw.WriteLine(tweetSinUrl);
                    }
                    count++;
                }
            }
            sw.Dispose();
        }
    }
}
