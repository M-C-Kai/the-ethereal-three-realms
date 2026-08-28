.class public final Lpmsj/work/e/af;
.super Lpmsj/work/d/c;


# instance fields
.field private final K:I

.field private final L:I

.field private final M:I

.field private final N:I

.field private final O:I

.field private final P:I

.field private final Q:I

.field private final R:I

.field private final S:I

.field private final T:I

.field private final U:I

.field private final V:I

.field private final W:I

.field private final X:I

.field private final Y:I

.field private final Z:I

.field private final a:I

.field private final aa:I

.field private final ab:I

.field private final ac:I

.field private ad:Lpmsj/work/d/l;

.field private ae:Lpmsj/work/d/a;

.field private af:Lpmsj/work/d/a;

.field private ag:Lpmsj/work/d/a;

.field private ah:Lpmsj/work/d/a;

.field private ai:Lpmsj/work/d/a;

.field private aj:Lpmsj/work/b/v;

.field private ak:Ljava/util/Vector;

.field private al:Lpmsj/work/a/i;

.field private am:Lpmsj/work/a/i;

.field private an:I

.field private ao:I

.field private ap:I

.field private final b:I

.field private final c:I

.field private final d:I

.field private final e:I

.field private final f:I


# direct methods
.method public constructor <init>()V
    .locals 3

    const/4 v2, 0x0

    const/16 v1, 0x4665

    invoke-direct {p0}, Lpmsj/work/d/c;-><init>()V

    const/16 v0, 0x4672

    iput v0, p0, Lpmsj/work/e/af;->a:I

    const/16 v0, 0x4673

    iput v0, p0, Lpmsj/work/e/af;->b:I

    const/16 v0, 0x4671

    iput v0, p0, Lpmsj/work/e/af;->c:I

    const/16 v0, 0x4651

    iput v0, p0, Lpmsj/work/e/af;->d:I

    const/16 v0, 0x4652

    iput v0, p0, Lpmsj/work/e/af;->e:I

    const/16 v0, 0x4653

    iput v0, p0, Lpmsj/work/e/af;->f:I

    const/16 v0, 0x4654

    iput v0, p0, Lpmsj/work/e/af;->K:I

    const/16 v0, 0x4655

    iput v0, p0, Lpmsj/work/e/af;->L:I

    const/16 v0, 0x4656

    iput v0, p0, Lpmsj/work/e/af;->M:I

    const/16 v0, 0x4657

    iput v0, p0, Lpmsj/work/e/af;->N:I

    const/16 v0, 0x4658

    iput v0, p0, Lpmsj/work/e/af;->O:I

    const/16 v0, 0x4659

    iput v0, p0, Lpmsj/work/e/af;->P:I

    const/16 v0, 0x465a

    iput v0, p0, Lpmsj/work/e/af;->Q:I

    const/16 v0, 0x465b

    iput v0, p0, Lpmsj/work/e/af;->R:I

    const/16 v0, 0x465c

    iput v0, p0, Lpmsj/work/e/af;->S:I

    const/16 v0, 0x465d

    iput v0, p0, Lpmsj/work/e/af;->T:I

    const/16 v0, 0x465e

    iput v0, p0, Lpmsj/work/e/af;->U:I

    const/16 v0, 0x4661

    iput v0, p0, Lpmsj/work/e/af;->V:I

    const/16 v0, 0x4664

    iput v0, p0, Lpmsj/work/e/af;->W:I

    iput v1, p0, Lpmsj/work/e/af;->X:I

    const/16 v0, 0x466e

    iput v0, p0, Lpmsj/work/e/af;->Y:I

    const/16 v0, 0x466f

    iput v0, p0, Lpmsj/work/e/af;->Z:I

    const/16 v0, 0x4670

    iput v0, p0, Lpmsj/work/e/af;->aa:I

    const/16 v0, 0x4650

    iput v0, p0, Lpmsj/work/e/af;->ab:I

    iput v1, p0, Lpmsj/work/e/af;->ac:I

    iput-object v2, p0, Lpmsj/work/e/af;->al:Lpmsj/work/a/i;

    iput-object v2, p0, Lpmsj/work/e/af;->am:Lpmsj/work/a/i;

    const/16 v0, 0xe

    iput v0, p0, Lpmsj/work/e/af;->an:I

    const/16 v0, 0x8

    iput v0, p0, Lpmsj/work/e/af;->ao:I

    const/16 v0, 0x9

    iput v0, p0, Lpmsj/work/e/af;->ap:I

    return-void
.end method

.method private C(I)V
    .locals 9

    const/4 v4, 0x0

    const/4 v3, 0x0

    invoke-static {}, Lpmsj/work/b/a;->e()Ljava/util/Vector;

    move-result-object v1

    new-instance v2, Ljava/util/Vector;

    const/4 v0, 0x2

    invoke-direct {v2, v0}, Ljava/util/Vector;-><init>(I)V

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v5

    invoke-virtual {p0}, Lpmsj/work/e/af;->ad()I

    move-result v0

    rem-int/lit8 v6, v0, 0x64

    move v7, v3

    :goto_0
    if-ge v7, v5, :cond_1

    invoke-virtual {v1, v7}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/j;

    invoke-virtual {v0}, Lpmsj/work/b/j;->b()Z

    move-result v8

    if-eqz v8, :cond_0

    check-cast v0, Lpmsj/work/b/g;

    iget v8, v0, Lpmsj/work/b/j;->f:I

    invoke-static {v8}, Lpmsj/work/b/j;->f(I)B

    move-result v8

    if-ne v8, v6, :cond_0

    invoke-virtual {v0}, Lpmsj/work/b/g;->j()Z

    move-result v8

    if-eqz v8, :cond_0

    invoke-virtual {v2, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_0
    add-int/lit8 v0, v7, 0x1

    move v7, v0

    goto :goto_0

    :cond_1
    invoke-direct {p0}, Lpmsj/work/e/af;->o()Lpmsj/work/b/g;

    move-result-object v0

    if-eqz v0, :cond_2

    invoke-virtual {v0}, Lpmsj/work/b/g;->c()Z

    move-result v1

    if-eqz v1, :cond_2

    move-object v6, v0

    :goto_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v7, 0x1

    move-object v1, p0

    move v5, p1

    move v8, v3

    invoke-virtual/range {v0 .. v8}, Lpmsj/work/d/n;->a(Lpmsj/work/d/c;Ljava/util/Vector;B[Ljava/lang/String;ILpmsj/work/b/g;IZ)Lpmsj/work/e/au;

    return-void

    :cond_2
    move-object v6, v4

    goto :goto_1
.end method

.method private D(I)Lpmsj/work/b/g;
    .locals 4

    iget-object v0, p0, Lpmsj/work/e/af;->ak:Ljava/util/Vector;

    if-eqz v0, :cond_1

    iget-object v0, p0, Lpmsj/work/e/af;->ak:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v1

    const/4 v0, 0x0

    move v2, v0

    :goto_0
    if-ge v2, v1, :cond_1

    iget-object v0, p0, Lpmsj/work/e/af;->ak:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/g;

    iget-byte v3, v0, Lpmsj/work/b/g;->k:B

    if-ne v3, p1, :cond_0

    :goto_1
    return-object v0

    :cond_0
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_0

    :cond_1
    const/4 v0, 0x0

    goto :goto_1
.end method

.method private a(Lpmsj/work/main/w;I)I
    .locals 7

    invoke-virtual {p1, p2}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    add-int/lit8 v1, p2, 0x1

    new-instance v2, Ljava/util/Vector;

    invoke-direct {v2}, Ljava/util/Vector;-><init>()V

    iput-object v2, p0, Lpmsj/work/e/af;->ak:Ljava/util/Vector;

    if-lez v0, :cond_0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v0, :cond_0

    mul-int/lit8 v3, v2, 0x6

    add-int/2addr v3, v1

    new-instance v4, Lpmsj/work/b/g;

    add-int/lit8 v5, v3, 0x4

    invoke-virtual {p1, v5}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v6

    invoke-direct {v4, v5, v6}, Lpmsj/work/b/g;-><init>(II)V

    add-int/lit8 v5, v3, 0x1

    invoke-virtual {p1, v5}, Lpmsj/work/main/w;->a(I)B

    move-result v5

    iput-byte v5, v4, Lpmsj/work/b/g;->k:B

    add-int/lit8 v5, v3, 0x2

    invoke-virtual {p1, v5}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v5

    iput-object v5, v4, Lpmsj/work/b/g;->o:Ljava/lang/String;

    add-int/lit8 v5, v3, 0x3

    invoke-virtual {p1, v5}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    int-to-byte v5, v5

    iput-byte v5, v4, Lpmsj/work/b/g;->n:B

    add-int/lit8 v3, v3, 0x5

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->b(I)S

    move-result v3

    iput-short v3, v4, Lpmsj/work/b/g;->q:S

    iget-object v3, p0, Lpmsj/work/e/af;->ak:Ljava/util/Vector;

    invoke-virtual {v3, v4}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_0
    mul-int/lit8 v0, v0, 0x6

    add-int/2addr v0, v1

    return v0
.end method

.method private i()Z
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    if-ne v0, v1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method private j()V
    .locals 3

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    if-eqz v0, :cond_0

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    iget-object v1, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->p()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-object v1, p0, Lpmsj/work/e/af;->ae:Lpmsj/work/d/a;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Lpmsj/work/d/a;->a_(Ljava/lang/String;)V

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->setLength(I)V

    iget-object v0, p0, Lpmsj/work/e/af;->af:Lpmsj/work/d/a;

    iget-object v1, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->F()La/a/d;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->a(La/a/d;)V

    :cond_0
    return-void
.end method

.method private k()V
    .locals 6

    const v5, 0x158e12

    const/4 v4, 0x0

    move v2, v4

    :goto_0
    iget v1, p0, Lpmsj/work/e/af;->an:I

    if-ge v2, v1, :cond_0

    add-int/lit16 v1, v2, 0x4651

    invoke-virtual {p0, v1}, Lpmsj/work/e/af;->w(I)Lpmsj/work/d/b;

    move-result-object v1

    check-cast v1, Lpmsj/work/d/a;

    invoke-virtual {v1}, Lpmsj/work/d/a;->f()V

    sget v3, La/c/x;->b:I

    invoke-virtual {v1, v3}, Lpmsj/work/d/a;->a(I)V

    new-instance v3, Lpmsj/work/a/i;

    invoke-direct {v3, v5}, Lpmsj/work/a/i;-><init>(I)V

    invoke-virtual {v1, v3}, Lpmsj/work/d/a;->b(Lpmsj/work/a/i;)V

    add-int/lit8 v1, v2, 0x1

    move v2, v1

    goto :goto_0

    :cond_0
    const/16 v1, 0x4661

    invoke-virtual {p0, v1}, Lpmsj/work/e/af;->w(I)Lpmsj/work/d/b;

    move-result-object v1

    check-cast v1, Lpmsj/work/d/a;

    invoke-virtual {v1}, Lpmsj/work/d/a;->f()V

    sget v2, La/c/x;->b:I

    invoke-virtual {v1, v2}, Lpmsj/work/d/a;->a(I)V

    new-instance v2, Lpmsj/work/a/i;

    invoke-direct {v2, v5}, Lpmsj/work/a/i;-><init>(I)V

    invoke-virtual {v1, v2}, Lpmsj/work/d/a;->b(Lpmsj/work/a/i;)V

    iget-object v1, p0, Lpmsj/work/e/af;->ak:Ljava/util/Vector;

    if-nez v1, :cond_1

    :goto_1
    return-void

    :cond_1
    iget-object v1, p0, Lpmsj/work/e/af;->ak:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v3

    :goto_2
    if-ge v4, v3, :cond_3

    iget-object v1, p0, Lpmsj/work/e/af;->ak:Ljava/util/Vector;

    invoke-virtual {v1, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v1

    move-object v0, v1

    check-cast v0, Lpmsj/work/b/g;

    move-object v2, v0

    iget-byte v1, v2, Lpmsj/work/b/g;->k:B

    add-int/lit16 v1, v1, 0x4650

    invoke-virtual {p0, v1}, Lpmsj/work/e/af;->w(I)Lpmsj/work/d/b;

    move-result-object v1

    check-cast v1, Lpmsj/work/d/a;

    if-eqz v1, :cond_2

    invoke-virtual {v1, v2}, Lpmsj/work/d/a;->a(Lpmsj/work/b/j;)V

    :cond_2
    add-int/lit8 v1, v4, 0x1

    move v4, v1

    goto :goto_2

    :cond_3
    invoke-direct {p0}, Lpmsj/work/e/af;->n()V

    goto :goto_1
.end method

.method private n()V
    .locals 7

    const/16 v6, 0x4665

    const/4 v5, 0x1

    iget-object v0, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->k()V

    const-string v0, ""

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->c(Ljava/lang/String;)V

    iget-object v0, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    iget v0, v0, Lpmsj/work/d/b;->g:I

    const/16 v1, 0x4650

    if-le v0, v1, :cond_0

    iget-object v0, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    iget v0, v0, Lpmsj/work/d/b;->g:I

    if-le v0, v6, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    iget-object v0, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    iget v0, v0, Lpmsj/work/d/b;->g:I

    rem-int/lit16 v0, v0, 0x4650

    invoke-direct {p0, v0}, Lpmsj/work/e/af;->D(I)Lpmsj/work/b/g;

    move-result-object v1

    if-nez v1, :cond_5

    const/4 v1, 0x0

    const/16 v2, 0xe

    new-array v2, v2, [Ljava/lang/String;

    const/4 v3, 0x0

    const-string v4, "\u5934\u76d4"

    aput-object v4, v2, v3

    const-string v3, "\u80a9\u7532"

    aput-object v3, v2, v5

    const/4 v3, 0x2

    const-string v4, "\u94e0\u7532"

    aput-object v4, v2, v3

    const/4 v3, 0x3

    const-string v4, "\u8170\u5e26"

    aput-object v4, v2, v3

    const/4 v3, 0x4

    const-string v4, "\u817f\u7532"

    aput-object v4, v2, v3

    const/4 v3, 0x5

    const-string v4, "\u9879\u94fe"

    aput-object v4, v2, v3

    const/4 v3, 0x6

    const-string v4, "\u62ab\u98ce"

    aput-object v4, v2, v3

    const/4 v3, 0x7

    const-string v4, "\u62a4\u8155"

    aput-object v4, v2, v3

    const/16 v3, 0x8

    const-string v4, "\u978b\u5b50"

    aput-object v4, v2, v3

    const/16 v3, 0x9

    const-string v4, "\u6b66\u5668"

    aput-object v4, v2, v3

    const/16 v3, 0xa

    const-string v4, "\u6212\u6307"

    aput-object v4, v2, v3

    const/16 v3, 0xb

    const-string v4, "\u5916\u5957"

    aput-object v4, v2, v3

    const/16 v3, 0xc

    const-string v4, "\u9970\u54c1"

    aput-object v4, v2, v3

    const/16 v3, 0xd

    const-string v4, "\u6cd5\u5b9d"

    aput-object v4, v2, v3

    iget-object v3, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    iget v3, v3, Lpmsj/work/d/b;->g:I

    const/16 v4, 0x465e

    if-gt v3, v4, :cond_2

    sub-int/2addr v0, v5

    aget-object v0, v2, v0

    :goto_1
    if-eqz v0, :cond_0

    iget-object v1, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    iget v2, p0, Lpmsj/work/e/af;->ao:I

    iget v3, p0, Lpmsj/work/e/af;->ap:I

    invoke-virtual {v1, v0, v2, v3}, Lpmsj/work/d/l;->a(Ljava/lang/String;II)Z

    goto :goto_0

    :cond_2
    const/16 v0, 0x4661

    iget-object v2, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    iget v2, v2, Lpmsj/work/d/b;->g:I

    if-ne v0, v2, :cond_3

    const-string v0, "\u5750\u9a91"

    goto :goto_1

    :cond_3
    const/16 v0, 0x4664

    iget-object v2, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    iget v2, v2, Lpmsj/work/d/b;->g:I

    if-ne v0, v2, :cond_4

    const-string v0, "\u7ea2\u7b26"

    goto :goto_1

    :cond_4
    iget-object v0, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    iget v0, v0, Lpmsj/work/d/b;->g:I

    if-ne v6, v0, :cond_7

    const-string v0, "\u9ec4\u7b26"

    goto :goto_1

    :cond_5
    invoke-direct {p0}, Lpmsj/work/e/af;->i()Z

    move-result v0

    if-eqz v0, :cond_6

    iget-object v0, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    iget v2, p0, Lpmsj/work/e/af;->ao:I

    iget v3, p0, Lpmsj/work/e/af;->ap:I

    invoke-static {v0, v1, p0, v2, v3}, Lpmsj/work/e/b;->a(Lpmsj/work/d/l;Lpmsj/work/b/j;Lpmsj/work/d/c;II)V

    goto/16 :goto_0

    :cond_6
    iget-object v0, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    invoke-virtual {v1}, Lpmsj/work/b/g;->q()Ljava/lang/String;

    move-result-object v2

    iget v3, p0, Lpmsj/work/e/af;->ao:I

    iget v4, p0, Lpmsj/work/e/af;->ap:I

    invoke-virtual {v0, v2, v3, v4}, Lpmsj/work/d/l;->a(Ljava/lang/String;II)Z

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->c()I

    move-result v0

    invoke-virtual {v1, v0}, Lpmsj/work/b/g;->l(I)Ljava/lang/String;

    move-result-object v0

    if-eqz v0, :cond_0

    iget-object v1, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    iget v2, p0, Lpmsj/work/e/af;->ao:I

    iget v3, p0, Lpmsj/work/e/af;->ap:I

    invoke-virtual {v1, v0, v2, v3}, Lpmsj/work/d/l;->a(Ljava/lang/String;II)Z

    goto/16 :goto_0

    :cond_7
    move-object v0, v1

    goto :goto_1
.end method

.method private o()Lpmsj/work/b/g;
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    iget v0, v0, Lpmsj/work/d/b;->g:I

    const/16 v1, 0x4650

    if-le v0, v1, :cond_0

    iget-object v0, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    iget v0, v0, Lpmsj/work/d/b;->g:I

    const/16 v1, 0x4665

    if-gt v0, v1, :cond_0

    iget-object v0, p0, Lpmsj/work/e/af;->s:Lpmsj/work/d/b;

    iget v0, v0, Lpmsj/work/d/b;->g:I

    rem-int/lit16 v0, v0, 0x4650

    invoke-direct {p0, v0}, Lpmsj/work/e/af;->D(I)Lpmsj/work/b/g;

    move-result-object v0

    :goto_0
    return-object v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method


# virtual methods
.method public final a(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 0

    return-void
.end method

.method public final a(Lpmsj/work/b/v;Ljava/util/Vector;)V
    .locals 0

    iput-object p1, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    iput-object p2, p0, Lpmsj/work/e/af;->ak:Ljava/util/Vector;

    invoke-virtual {p0}, Lpmsj/work/e/af;->ag()V

    return-void
.end method

.method public final a(Lpmsj/work/main/w;)V
    .locals 10

    const/16 v9, 0x11

    const/4 v8, 0x3

    const/4 v7, 0x2

    const/4 v6, 0x1

    const/4 v2, 0x0

    invoke-virtual {p1, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    iget-object v0, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    sget v1, Lpmsj/work/a/c;->ac:I

    add-int/lit8 v1, v1, 0x3

    mul-int/lit8 v1, v1, 0x2

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->j(I)V

    iget-object v0, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    invoke-virtual {v0, v2}, Lpmsj/work/d/l;->b(Z)V

    invoke-virtual {p0}, Lpmsj/work/e/af;->ag()V

    :goto_1
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {p1, v6}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/m;->n(I)Lpmsj/work/b/v;

    move-result-object v0

    iput-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    if-nez v0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/af;->ae()V

    goto :goto_1

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x36

    invoke-virtual {p1, v7}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x4b

    invoke-virtual {p1, v8}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    const/4 v0, 0x4

    invoke-direct {p0, p1, v0}, Lpmsj/work/e/af;->a(Lpmsj/work/main/w;I)I

    move-result v0

    iget-object v1, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v3, 0x4f

    add-int/lit8 v4, v0, 0x1

    invoke-virtual {p1, v0}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v0

    invoke-virtual {v1, v3, v0}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x54

    invoke-virtual {p1, v4}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    goto :goto_0

    :pswitch_1
    invoke-virtual {p1, v7}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    invoke-virtual {p1, v9}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/v;->H(I)I

    move-result v3

    new-instance v0, Lpmsj/work/b/v;

    invoke-virtual {p1, v6}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    move v5, v2

    invoke-direct/range {v0 .. v5}, Lpmsj/work/b/v;-><init>(IBIIZ)V

    iput-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    invoke-virtual {p1, v6}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v1

    invoke-virtual {v0, v6, v1}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/4 v1, 0x6

    invoke-virtual {v0, v1, v4}, Lpmsj/work/b/v;->a(BI)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/4 v1, 0x7

    invoke-virtual {p1, v8}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/4 v1, 0x4

    invoke-virtual {p1, v1}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v1

    invoke-virtual {v0, v8, v1}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/4 v1, 0x5

    invoke-virtual {p1, v1}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v1

    invoke-virtual {v0, v7, v1}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0xa

    const/4 v3, 0x6

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0xb

    const/4 v3, 0x7

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0xc

    const/16 v3, 0x8

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0xe

    const/16 v3, 0x9

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0xf

    const/16 v3, 0xa

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x10

    const/16 v3, 0xb

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0xc

    invoke-virtual {p1, v1}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v1

    invoke-virtual {v0, v9, v1}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x12

    const/16 v3, 0xd

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x13

    const/16 v3, 0xe

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x14

    const/16 v3, 0xf

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x15

    const/16 v3, 0x10

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x16

    invoke-virtual {p1, v9}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x36

    const/16 v3, 0x12

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v1, 0x4b

    const/16 v3, 0x13

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v1, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    iget-object v1, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v3, 0x16

    invoke-virtual {v1, v3}, Lpmsj/work/b/v;->f(B)I

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/v;->I(I)V

    iget-object v0, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    invoke-virtual {v0}, Lpmsj/work/b/v;->r()V

    const/16 v0, 0x14

    invoke-direct {p0, p1, v0}, Lpmsj/work/e/af;->a(Lpmsj/work/main/w;I)I

    move-result v0

    iget-object v1, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    const/16 v3, 0x4f

    invoke-virtual {p1, v0}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v0

    invoke-virtual {v1, v3, v0}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    goto/16 :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_0
        :pswitch_1
    .end packed-switch
.end method

.method public final a(Lpmsj/work/b/j;)Z
    .locals 5

    const/16 v4, 0x3f1

    const/4 v3, 0x0

    invoke-direct {p0}, Lpmsj/work/e/af;->i()Z

    move-result v0

    if-eqz v0, :cond_1

    iget-byte v0, p1, Lpmsj/work/b/j;->n:B

    iget-object v1, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->c()I

    move-result v1

    if-le v0, v1, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u7b49\u7ea7\u4e0d\u8db3\uff0c\u65e0\u6cd5\u88c5\u5907\u3002"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v3

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x5

    iget v1, p1, Lpmsj/work/b/j;->e:I

    invoke-static {v4, v0, v1}, Lpmsj/work/main/w;->a(ISI)V

    const/4 v0, 0x1

    goto :goto_0

    :cond_1
    const/16 v0, 0x51

    iget v1, p1, Lpmsj/work/b/j;->e:I

    iget-object v2, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    invoke-virtual {v2}, Lpmsj/work/b/v;->u()I

    move-result v2

    invoke-static {v4, v0, v1, v2}, Lpmsj/work/main/w;->a(ISII)V

    move v0, v3

    goto :goto_0
.end method

.method public final ag()V
    .locals 0

    invoke-direct {p0}, Lpmsj/work/e/af;->j()V

    invoke-direct {p0}, Lpmsj/work/e/af;->k()V

    return-void
.end method

.method public final b(Lpmsj/work/b/j;)V
    .locals 1

    iget v0, p1, Lpmsj/work/b/j;->f:I

    invoke-static {v0}, Lpmsj/work/b/j;->f(I)B

    move-result v0

    add-int/lit16 v0, v0, 0x4650

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->x(I)V

    iget v0, p1, Lpmsj/work/b/j;->e:I

    invoke-direct {p0, v0}, Lpmsj/work/e/af;->C(I)V

    return-void
.end method

.method public final b(Lpmsj/work/b/v;Ljava/util/Vector;)V
    .locals 0

    iput-object p1, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    iput-object p2, p0, Lpmsj/work/e/af;->ak:Ljava/util/Vector;

    invoke-direct {p0}, Lpmsj/work/e/af;->j()V

    invoke-direct {p0}, Lpmsj/work/e/af;->k()V

    return-void
.end method

.method public final b(Lpmsj/work/d/b;)V
    .locals 5

    const/4 v4, 0x0

    iget v0, p1, Lpmsj/work/d/b;->g:I

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    invoke-direct {p0}, Lpmsj/work/e/af;->o()Lpmsj/work/b/g;

    move-result-object v0

    if-eqz v0, :cond_0

    iget-object v1, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    iget v2, p0, Lpmsj/work/e/af;->ao:I

    iget v3, p0, Lpmsj/work/e/af;->ap:I

    invoke-static {v1, v0, v2, v3}, Lpmsj/work/e/b;->a(Lpmsj/work/d/l;Lpmsj/work/b/j;II)V

    goto :goto_0

    :cond_0
    const/16 v0, 0x4651

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->x(I)V

    goto :goto_0

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x8

    new-array v1, v1, [Ljava/lang/String;

    const-string v2, "\u88c5\u5907\u5f3a\u5316"

    aput-object v2, v1, v4

    const/4 v2, 0x1

    const-string v3, "\u5f3a\u5316\u8f6c\u79fb"

    aput-object v3, v1, v2

    const/4 v2, 0x2

    const-string v3, "\u4e94\u884c\u953b\u9020"

    aput-object v3, v1, v2

    const/4 v2, 0x3

    const-string v3, "\u4e94\u884c\u8f6c\u79fb"

    aput-object v3, v1, v2

    const/4 v2, 0x4

    const-string v3, "\u88c5\u5907\u5f00\u5b54"

    aput-object v3, v1, v2

    const/4 v2, 0x5

    const-string v3, "\u5b9d\u77f3\u9576\u5d4c"

    aput-object v3, v1, v2

    const/4 v2, 0x6

    const-string v3, "\u5b9d\u77f3\u62c6\u9664"

    aput-object v3, v1, v2

    const/4 v2, 0x7

    const-string v3, "\u88c5\u5907\u6253\u9020"

    aput-object v3, v1, v2

    invoke-virtual {v0, v1, v4, p0}, Lpmsj/work/d/n;->a([Ljava/lang/String;ILpmsj/work/d/c;)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x160

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto :goto_0

    :pswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8be5\u529f\u80fd\u6682\u672a\u5f00\u653e"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x466e
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_0
    .end packed-switch
.end method

.method public final b(Ljava/lang/String;)Z
    .locals 5

    const/4 v4, 0x0

    const/16 v3, 0x3f1

    const/16 v1, 0x144

    const/4 v2, 0x1

    const-string v0, "\u67e5\u770b"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_2

    invoke-direct {p0}, Lpmsj/work/e/af;->o()Lpmsj/work/b/g;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-direct {p0}, Lpmsj/work/e/af;->i()Z

    move-result v1

    if-eqz v1, :cond_1

    iget v0, v0, Lpmsj/work/b/g;->e:I

    invoke-static {v0}, Lpmsj/work/main/e;->c(I)V

    :cond_0
    :goto_0
    return v2

    :cond_1
    iget v0, v0, Lpmsj/work/b/j;->e:I

    iget-object v1, p0, Lpmsj/work/e/af;->aj:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->u()I

    move-result v1

    invoke-static {v0, v1}, Lpmsj/work/main/e;->a(II)V

    goto :goto_0

    :cond_2
    const-string v0, "\u5378\u4e0b"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_3

    invoke-direct {p0}, Lpmsj/work/e/af;->o()Lpmsj/work/b/g;

    move-result-object v0

    if-eqz v0, :cond_0

    const/4 v1, 0x6

    iget v0, v0, Lpmsj/work/b/g;->e:I

    invoke-static {v3, v1, v0}, Lpmsj/work/main/w;->a(ISI)V

    goto :goto_0

    :cond_3
    const-string v0, "\u66f4\u6362"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_4

    invoke-direct {p0, v4}, Lpmsj/work/e/af;->C(I)V

    goto :goto_0

    :cond_4
    const-string v0, "\u89e3\u5c01"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_5

    invoke-direct {p0}, Lpmsj/work/e/af;->o()Lpmsj/work/b/g;

    move-result-object v0

    if-eqz v0, :cond_0

    const/16 v1, 0x4c

    iget v0, v0, Lpmsj/work/b/j;->e:I

    invoke-static {v3, v1, v0}, Lpmsj/work/main/w;->a(ISI)V

    goto :goto_0

    :cond_5
    const-string v0, "\u4f20\u9001"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_6

    const/16 v0, 0x41

    invoke-static {v3, v0}, Lpmsj/work/main/w;->a(IS)V

    goto :goto_0

    :cond_6
    const-string v0, "\u88c5\u5907\u5f3a\u5316"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_7

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x185

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/bw;

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    const/4 v0, 0x4

    invoke-virtual {p0, v0}, Lpmsj/work/e/bw;->y(I)V

    goto :goto_0

    :cond_7
    const-string v0, "\u5f3a\u5316\u8f6c\u79fb"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_8

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x186

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/eb;

    invoke-virtual {p0, v4}, Lpmsj/work/e/eb;->y(I)V

    goto/16 :goto_0

    :cond_8
    const-string v0, "\u4e94\u884c\u953b\u9020"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_9

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x67

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ah;

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    invoke-virtual {p0, v2}, Lpmsj/work/e/ah;->y(I)V

    goto/16 :goto_0

    :cond_9
    const-string v0, "\u4e94\u884c\u8f6c\u79fb"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_a

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8be5\u529f\u80fd\u6682\u672a\u5f00\u653e"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto/16 :goto_0

    :cond_a
    const-string v0, "\u88c5\u5907\u5f00\u5b54"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_b

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ag;

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    invoke-virtual {p0, v2}, Lpmsj/work/e/ag;->y(I)V

    goto/16 :goto_0

    :cond_b
    const-string v0, "\u5b9d\u77f3\u9576\u5d4c"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_c

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ag;

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    const/4 v0, 0x3

    invoke-virtual {p0, v0}, Lpmsj/work/e/ag;->y(I)V

    goto/16 :goto_0

    :cond_c
    const-string v0, "\u5b9d\u77f3\u62c6\u9664"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_d

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ag;

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    const/16 v0, 0x9

    invoke-virtual {p0, v0}, Lpmsj/work/e/ag;->y(I)V

    goto/16 :goto_0

    :cond_d
    const-string v0, "\u88c5\u5907\u6253\u9020"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x154

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ao;

    const/16 v0, 0x898

    invoke-virtual {p0, v0}, Lpmsj/work/e/ao;->y(I)V

    goto/16 :goto_0
.end method

.method protected final c()V
    .locals 6

    const/16 v5, 0x4671

    const/4 v2, 0x0

    const/4 v4, 0x3

    const/4 v3, 0x1

    invoke-virtual {p0, v5}, Lpmsj/work/e/af;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    iget-object v0, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    const v1, 0x8000a

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->l(I)V

    iget-object v0, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->o()V

    iget-object v0, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    sget v1, La/c/x;->b:I

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a(I)V

    iget-object v0, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->c()V

    const/16 v0, 0x4672

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/e/af;->ae:Lpmsj/work/d/a;

    const/4 v0, 0x7

    invoke-virtual {p0, v0, v5}, Lpmsj/work/e/af;->h(II)V

    const/16 v0, 0x4673

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/e/af;->af:Lpmsj/work/d/a;

    iget-object v0, p0, Lpmsj/work/e/af;->al:Lpmsj/work/a/i;

    if-nez v0, :cond_0

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x147790

    invoke-direct {v0, v1, v2}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/e/af;->al:Lpmsj/work/a/i;

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/af;->am:Lpmsj/work/a/i;

    if-nez v0, :cond_1

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x147664

    invoke-direct {v0, v1, v2}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/e/af;->am:Lpmsj/work/a/i;

    :cond_1
    const/16 v0, 0x466e

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/e/af;->ag:Lpmsj/work/d/a;

    iget-object v0, p0, Lpmsj/work/e/af;->ag:Lpmsj/work/d/a;

    iget-object v1, p0, Lpmsj/work/e/af;->al:Lpmsj/work/a/i;

    iget-object v2, p0, Lpmsj/work/e/af;->am:Lpmsj/work/a/i;

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/a;->a(Lpmsj/work/a/i;Lpmsj/work/a/i;)V

    iget-object v0, p0, Lpmsj/work/e/af;->ag:Lpmsj/work/d/a;

    const-string v1, "\u88c5\u5907\u8fdb\u9636"

    invoke-virtual {v0, v1, v3, v4}, Lpmsj/work/d/a;->a(Ljava/lang/String;II)V

    const/16 v0, 0x466f

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/e/af;->ah:Lpmsj/work/d/a;

    iget-object v0, p0, Lpmsj/work/e/af;->ah:Lpmsj/work/d/a;

    iget-object v1, p0, Lpmsj/work/e/af;->al:Lpmsj/work/a/i;

    iget-object v2, p0, Lpmsj/work/e/af;->am:Lpmsj/work/a/i;

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/a;->a(Lpmsj/work/a/i;Lpmsj/work/a/i;)V

    iget-object v0, p0, Lpmsj/work/e/af;->ah:Lpmsj/work/d/a;

    const-string v1, "\u9a91\u4e58\u56fe\u9274"

    invoke-virtual {v0, v1, v3, v4}, Lpmsj/work/d/a;->a(Ljava/lang/String;II)V

    const/16 v0, 0x4670

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/e/af;->ai:Lpmsj/work/d/a;

    iget-object v0, p0, Lpmsj/work/e/af;->ai:Lpmsj/work/d/a;

    iget-object v1, p0, Lpmsj/work/e/af;->al:Lpmsj/work/a/i;

    iget-object v2, p0, Lpmsj/work/e/af;->am:Lpmsj/work/a/i;

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/a;->a(Lpmsj/work/a/i;Lpmsj/work/a/i;)V

    iget-object v0, p0, Lpmsj/work/e/af;->ai:Lpmsj/work/d/a;

    const-string v1, "\u6cd5\u5b9d\u56fe\u9274"

    invoke-virtual {v0, v1, v3, v4}, Lpmsj/work/d/a;->a(Ljava/lang/String;II)V

    const/16 v0, 0x4651

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->x(I)V

    const/16 v0, 0x8

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->q(I)V

    const/16 v0, 0x10

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->q(I)V

    const-string v0, "*\u952e\u6216\u70b9\u51fb\u5207\u6362\u5c5e\u6027"

    invoke-virtual {p0, v0}, Lpmsj/work/e/af;->c(Ljava/lang/String;)V

    return-void
.end method

.method protected final c(Lpmsj/work/d/b;)V
    .locals 4

    const/4 v2, 0x0

    const-string v3, "\u67e5\u770b"

    iget v0, p1, Lpmsj/work/d/b;->g:I

    const/16 v1, 0x4650

    if-le v0, v1, :cond_2

    iget v0, p1, Lpmsj/work/d/b;->g:I

    const/16 v1, 0x4665

    if-gt v0, v1, :cond_2

    invoke-direct {p0}, Lpmsj/work/e/af;->o()Lpmsj/work/b/g;

    move-result-object v0

    invoke-direct {p0}, Lpmsj/work/e/af;->i()Z

    move-result v1

    if-eqz v1, :cond_4

    if-eqz v0, :cond_3

    new-instance v1, Ljava/util/Vector;

    invoke-direct {v1}, Ljava/util/Vector;-><init>()V

    const/16 v2, 0x40

    invoke-virtual {v0, v2}, Lpmsj/work/b/g;->e(I)Z

    move-result v2

    if-eqz v2, :cond_0

    const-string v2, "\u4f20\u9001"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_0
    const-string v2, "\u67e5\u770b"

    invoke-virtual {v1, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u66f4\u6362"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u5378\u4e0b"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const/16 v2, 0x20

    invoke-virtual {v0, v2}, Lpmsj/work/b/j;->e(I)Z

    move-result v0

    if-eqz v0, :cond_1

    const-string v0, "\u89e3\u5c01"

    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1, p0}, Lpmsj/work/d/n;->a(Ljava/util/Vector;Lpmsj/work/d/c;)V

    :cond_2
    :goto_0
    return-void

    :cond_3
    invoke-direct {p0, v2}, Lpmsj/work/e/af;->C(I)V

    goto :goto_0

    :cond_4
    if-eqz v0, :cond_2

    const/4 v0, 0x1

    new-array v0, v0, [Ljava/lang/String;

    const-string v1, "\u67e5\u770b"

    aput-object v3, v0, v2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v0, p0}, Lpmsj/work/d/n;->a([Ljava/lang/String;Lpmsj/work/d/c;)V

    goto :goto_0
.end method

.method public final d(Lpmsj/work/d/b;)V
    .locals 0

    invoke-direct {p0}, Lpmsj/work/e/af;->n()V

    return-void
.end method
