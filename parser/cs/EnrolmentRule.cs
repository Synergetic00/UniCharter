
//#define IGNORE_UNNECESSARY

using System;
using Macquarie.Handbook.Data.Helpers;
using Macquarie.Handbook.Data.Shared;
using Newtonsoft.Json;

namespace Macquarie.Handbook.Data.Unit.Prerequisites
{
    public class EnrolmentRule
    {
        private string description;

        [JsonProperty("description")]
        public string Description { get => description; set => description = HTMLTagStripper.StripHtmlTags(value); }
        [JsonProperty("type")]
        public LabelledValue Type { get; set; }
#if IGNORE_UNNECESSARY
        [JsonIgnore]
#else
        [JsonProperty("cl_id")]
#endif
        public string CL_ID { get; set; }
        #if IGNORE_UNNECESSARY
        [JsonIgnore]
#else
        [JsonProperty("order")]
#endif
        public UInt16 Order { get; set; }

        public override string ToString() {
            return Description;
        }
    }
}