using System.Collections.Generic;

namespace Macquarie.Handbook.Data.Unit.Prerequisites
{
    public class CompoundEnrolmentRule : EnrolmentRule
    {
        public CompoundType RuleCompoundType { get; init; }
        public List<EnrolmentRule> Rules {get; init;}
    }

    public enum CompoundType
    {
        AND,
        OR
    }

}